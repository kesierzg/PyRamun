import random

STAGE_MULTIPLIERS = {
    -6: (25, 100),
    -5: (28, 100),
    -4: (33, 100),
    -3: (40, 100),
    -2: (50, 100),
    -1: (66, 100),
     0: (1,  1),
     1: (15, 10),
     2: (2,  1),
     3: (25, 10),
     4: (3,  1),
     5: (35, 10),
     6: (4,  1),
}

def apply_stage(base_value, stage):
    stage = max(-6, min(6, stage))
    num, den = STAGE_MULTIPLIERS[stage]
    return max(1, int(base_value * num / den))


class CombatantStatus:
    def __init__(self):
        self.primary = None
        self.confusion = False
        self.confusion_turns = 0
        self.toxic_counter = 1
        self.sleep_turns = 0
        self.stat_stages = {"atk": 0, "def": 0, "spc": 0, "spd": 0, "acc": 0, "eva": 0}
        self.last_move: str = ""
        self.disabled_move: str = ""
        self.disable_turns: int = 0
        self.flinched: bool = False

    def reset(self):
        self.__init__()

    def try_apply_primary(self, status):
        if self.primary is not None:
            return False
        self.primary = status
        if status == "sleep":
            self.sleep_turns = random.randint(1, 7)
        if status == "bad_poison":
            self.toxic_counter = 1
        return True

    def apply_confusion(self, min_turns=2, max_turns=5):
        if not self.confusion:
            self.confusion = True
            self.confusion_turns = random.randint(min_turns, max_turns)
            return True
        return False

    def change_stat(self, stat, delta):
        old = self.stat_stages.get(stat, 0)
        new = max(-6, min(6, old + delta))
        self.stat_stages[stat] = new
        return new - old, new

    def effective_stat(self, stat_name, base_stats):
        base = base_stats[stat_name]
        stage = self.stat_stages.get(stat_name, 0)
        value = apply_stage(base, stage)

        if stat_name == "atk" and self.primary == "burn":
            value = value // 2
        if stat_name == "spd" and self.primary == "paralysis":
            value = value // 4

        return max(1, value)

    def effective_accuracy(self):
        num, den = STAGE_MULTIPLIERS[self.stat_stages.get("acc", 0)]
        return num / den

    def effective_evasiveness(self):
        num, den = STAGE_MULTIPLIERS[self.stat_stages.get("eva", 0)]
        return num / den

    def resolve_before_move(self, name=""):
        messages = []
        can_move = True

        if self.disable_turns > 0:
            self.disable_turns -= 1
            if self.disable_turns == 0:
                expired = self.disabled_move
                self.disabled_move = ""
                messages.append(f"{expired} is no longer disabled!")

        if self.primary == "sleep":
            if self.sleep_turns > 0:
                messages.append(f"{name} is fast asleep!")
                self.sleep_turns -= 1
                can_move = False
            else:
                messages.append(f"{name} woke up!")
                self.primary = None

        elif self.primary == "freeze":
            thaw_roll = random.randint(1, 100)
            if thaw_roll <= 20:
                messages.append(f"{name} thawed out!")
                self.primary = None
            else:
                messages.append(f"{name} is frozen solid!")
                can_move = False

        elif self.primary == "paralysis":
            if random.randint(1, 4) == 1:
                messages.append(f"{name} is fully paralyzed!")
                can_move = False

        if can_move and self.confusion:
            self.confusion_turns -= 1
            if self.confusion_turns <= 0:
                self.confusion = False
                messages.append(f"{name} snapped out of confusion!")
            else:
                messages.append(f"{name} is confused!")
                if random.randint(1, 2) == 1:
                    messages.append(f"{name} hurt itself in confusion!")
                    can_move = False

        return can_move, messages

    def resolve_end_of_turn(self, max_hp, name=""):
        messages = []
        damage = 0

        if self.primary == "poison":
            damage = max(1, max_hp // 8)
            messages.append(f"{name} is hurt by poison!")

        elif self.primary == "bad_poison":
            damage = max(1, (max_hp * self.toxic_counter) // 16)
            self.toxic_counter += 1
            messages.append(f"{name} is hurt by poison!")

        elif self.primary == "burn":
            damage = max(1, max_hp // 8)
            messages.append(f"{name} is hurt by the burn!")

        return damage, messages

    def status_label(self):
        labels = {
            "poison":    "PSN",
            "bad_poison": "PSN",
            "paralysis": "PAR",
            "freeze":    "FRZ",
            "burn":      "BRN",
            "sleep":     "SLP",
        }
        return labels.get(self.primary, "")
