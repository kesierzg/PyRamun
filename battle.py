import random
from attacks import ATTACKS, PYRAMUN_TYPES, get_multiplier
from status import CombatantStatus

def _hits(attack, attacker_status, defender_status):
    if attack.get("never_misses"):
        return True
    base_acc = attack.get("accuracy", 100)
    acc_mod  = attacker_status.effective_accuracy()
    eva_mod  = defender_status.effective_evasiveness()
    final_acc = base_acc * acc_mod / eva_mod
    return random.randint(1, 100) <= final_acc


def calculate_damage(attack, attacker_stats, defender_stats,
                     attacker_status, defender_status, defender_pyramun):

    if not _hits(attack, attacker_status, defender_status):
        return None, None

    if attack.get("power", 0) == 0 and "fixed_damage" not in attack:
        return [], None

    hit_min, hit_max = attack.get("hits", (1, 1))
    hit_count = random.randint(hit_min, hit_max)

    #dragonrage
    if "fixed_damage" in attack:
        return [attack["fixed_damage"]] * hit_count, None

    if attack["category"] == "physical":
        atk  = attacker_status.effective_stat("atk", attacker_stats)
        defn = defender_status.effective_stat("def", defender_stats)
    else:
        atk  = attacker_status.effective_stat("spc", attacker_stats)
        defn = defender_status.effective_stat("spc", defender_stats)

    power       = attack["power"]
    base_damage = int((atk / defn) * power)
    base_damage = int(base_damage * random.uniform(0.85, 1.0))

    mult        = get_multiplier(attack["type"], PYRAMUN_TYPES[defender_pyramun])
    base_damage = int(base_damage * mult)
    base_damage = max(1, base_damage)

    return [base_damage] * hit_count, mult


def apply_effect(attack, target_status, user_status, messages, target_moves=None, target_name=""):
    effect = attack.get("effect")
    if not effect:
        return

    chance = attack.get("effect_chance", 100)
    if random.randint(1, 100) > chance:
        return

    targets_self = attack.get("targets_self", False)
    subject      = user_status if targets_self else target_status
    value        = attack.get("effect_value", 1)

    if effect in ("poison", "bad_poison", "paralysis", "burn", "freeze", "sleep"):
        if subject.try_apply_primary(effect):
            labels = {
                "poison":     "was poisoned!",
                "bad_poison": "was badly poisoned!",
                "paralysis":  "is paralyzed! It may not move!",
                "burn":       "was burned!",
                "freeze":     "was frozen solid!",
                "sleep":      "fell asleep!",
            }
            messages.append(f"{target_name} {labels[effect]}")
        else:
            messages.append("But it failed!")

    elif effect == "confusion":
        if target_status.apply_confusion():
            messages.append(f"{target_name} became confused!")
        else:
            messages.append("But it failed!")

    elif effect == "swagger":
        target_status.change_stat("atk", value)
        messages.append(f"{target_name}'s Attack rose sharply!")
        if target_status.apply_confusion():
            messages.append(f"{target_name} became confused!")

    elif effect.startswith("lower_"):
        stat = effect[len("lower_"):]
        delta, _ = subject.change_stat(stat, -value)
        _stat_message(stat, delta, messages) if delta != 0 else messages.append("But it failed!")

    elif effect.startswith("raise_"):
        stat = effect[len("raise_"):]
        delta, _ = subject.change_stat(stat, value)
        _stat_message(stat, delta, messages) if delta != 0 else messages.append("But it failed!")

    elif effect == "flinch":
        target_status.flinched = True

    elif effect == "disable":
        if not target_status.disabled_move:
            candidate = target_status.last_move or (
                random.choice(target_moves)["name"] if target_moves else None
            )
            if candidate:
                target_status.disabled_move = candidate
                target_status.disable_turns = random.randint(3, 7)
                messages.append(f"{candidate} was disabled!")
            else:
                messages.append("But it failed!")
        else:
            messages.append("But it failed!")

def _stat_message(stat, delta, messages):
    names = {
        "atk": "Attack", "def": "Defense", "spc": "Special",
        "spd": "Speed",  "acc": "Accuracy", "eva": "Evasiveness",
    }
    name   = names.get(stat, stat.capitalize())
    sharp  = abs(delta) >= 2
    if delta > 0:
        suffix = "sharply rose!" if sharp else "rose!"
    else:
        suffix = "harshly fell!" if sharp else "fell!"
    messages.append(f"{name} {suffix}")


class BattleState:
    def __init__(self):
        self.player_hp        = 0
        self.enemy_hp         = 0
        self.player_stats     = None
        self.enemy_stats      = None
        self.selected_pyramun = None
        self.enemy_pyramun    = None

        self.player_status    = CombatantStatus()
        self.enemy_status     = CombatantStatus()

        self.pending_attack   = None
        self.battle_message   = ""
        self.message_timer    = 0
        self.message_phase    = 0

        self._msg_queue: list = []
        self.enemy_pending_attack = None
        self.player_went_first = True
        self.last_fainted = ""

        self._wind_up_shown = False

        self._mh_queue: list = []
        self._mh_total  = 0
        self._mh_side   = "enemy"
        self._mh_mult   = None
        self._mh_next   = 8

    def setup(self, selected_pyramun, enemy_pyramun, player_stats, enemy_stats):
        self.selected_pyramun = selected_pyramun
        self.enemy_pyramun    = enemy_pyramun
        self.player_stats     = player_stats
        self.enemy_stats      = enemy_stats
        self.player_hp        = player_stats["hp"]
        self.enemy_hp         = enemy_stats["hp"]
        self.player_status.reset()
        self.enemy_status.reset()

    def setup_next_enemy(self, enemy_pyramun, enemy_stats):
        self.enemy_pyramun = enemy_pyramun
        self.enemy_stats   = enemy_stats
        self.enemy_hp      = enemy_stats["hp"]
        self.enemy_status.reset()
        self._msg_queue.clear()
        self.battle_message = f"Enemy sends out {enemy_pyramun}!"
        self.message_timer  = 90
        self.message_phase  = 6

    def setup_voluntary_switch(self, selected_pyramun, player_stats):
        self.selected_pyramun = selected_pyramun
        self.player_stats = player_stats
        self.player_hp = player_stats["hp"]
        self.player_status.reset()
        self._msg_queue.clear()
        self.pending_attack = None
        self.enemy_pending_attack = None
        self.player_went_first = True
        self.battle_message = f"Go! {selected_pyramun}!"
        self.message_timer = 90
        self.message_phase = 7

    def setup_next_player(self, selected_pyramun, player_stats):
        self.selected_pyramun = selected_pyramun
        self.player_stats     = player_stats
        self.player_hp        = player_stats["hp"]
        self.player_status.reset()
        self._msg_queue.clear()
        self.battle_message = f"Go! {selected_pyramun}!"
        self.message_timer  = 90
        self.message_phase  = 6

    def _enqueue(self, *messages):
        self._msg_queue.extend(m for m in messages if m)

    def _show_next(self, timer=60):
        if self._msg_queue:
            self.battle_message = self._msg_queue.pop(0)
            self.message_timer  = timer
            return True
        return False

    def _pick_enemy_move(self):
        attacks = ATTACKS[self.enemy_pyramun]
        weights = [3 if a.get("weight", 0) == 0 else 1 for a in attacks]
        pairs = [(a, w) for a, w in zip(attacks, weights)
                 if a["name"] != self.enemy_status.disabled_move]
        if not pairs:
            pairs = list(zip(attacks, weights))
        avail_a, avail_w = zip(*pairs)
        self.enemy_pending_attack = random.choices(avail_a, weights=avail_w, k=1)[0]

    def start_turn(self, attack):
        self.pending_attack = attack
        self._pick_enemy_move()

        player_priority = attack.get("priority", 0)
        enemy_priority  = self.enemy_pending_attack.get("priority", 0)

        if player_priority != enemy_priority:
            player_first = player_priority > enemy_priority
        else:
            player_spd = self.player_status.effective_stat("spd", self.player_stats)
            enemy_spd  = self.enemy_status.effective_stat("spd", self.enemy_stats)
            player_first = player_spd >= enemy_spd

        self.player_went_first = player_first
        if player_first:
            self.message_phase  = 0
            self.battle_message = f"Your {self.selected_pyramun} used {attack['name']}!"
            self.message_timer  = 90
            return "player_attack"
        else:
            self.message_phase  = 7
            self.battle_message = ""
            self.message_timer  = 1
            return "enemy_attack"

    def advance(self, anim):
        self.message_timer -= 1
        if self.message_timer > 0:
            return None

        if self._msg_queue:
            self._show_next()
            return None

        return self._run_phase(self.message_phase, anim)

    def _run_phase(self, phase, anim):
        if phase == 0:
            can_move, pre_msgs = self.player_status.resolve_before_move(f"Your {self.selected_pyramun}")
            if pre_msgs:
                self._enqueue(*pre_msgs)

            if not can_move:
                if pre_msgs and "hurt itself" in "".join(pre_msgs):
                    self.player_hp = max(0, self.player_hp - max(1, self.player_hp // 8))
                    if self.player_hp == 0:
                        pre_msgs.append(f"Your {self.selected_pyramun} fainted!")
                        self._enqueue(*pre_msgs)
                        self.message_phase = 2
                        self._show_next(timer=120)
                        return None
                self.message_phase = 8
                if not self._show_next():
                    self.message_timer = 1
                return None

            if self.player_status.disabled_move == self.pending_attack["name"]:
                self._enqueue(f"{self.pending_attack['name']} is disabled!")
                self.message_phase = 8
                self._show_next()
                return None

            self.player_status.last_move = self.pending_attack["name"]

            hit_damages, mult = calculate_damage(
                self.pending_attack,
                self.player_stats, self.enemy_stats,
                self.player_status, self.enemy_status,
                self.enemy_pyramun,
            )

            messages = []

            if hit_damages is None:
                messages.append(f"{self.selected_pyramun}'s attack missed!")
                self._enqueue(*messages)
                self.message_phase = 8
                self._show_next()
                return None

            total_damage = sum(hit_damages)
            hit_count    = len(hit_damages)

            if hit_count > 1:
                self._mh_queue = list(hit_damages)
                self._mh_total = hit_count
                self._mh_side  = "enemy"
                self._mh_mult  = mult
                self._mh_next  = 8
                self.message_phase  = 10
                self.message_timer  = 1
                return None

            if total_damage > 0:
                self.enemy_hp = max(0, self.enemy_hp - total_damage)
                anim.trigger_blink("enemy")

                if mult is not None and mult != 1:
                    if   mult == 0: messages.append("It had no effect!")
                    elif mult > 1:  messages.append("It's super effective!")
                    else:           messages.append("It's not very effective...")

            if hit_damages is not None and self.enemy_hp > 0:
                apply_effect(self.pending_attack, self.enemy_status, self.player_status, messages,
                             target_moves=ATTACKS[self.enemy_pyramun],
                             target_name=f"Enemy {self.enemy_pyramun}")

            if self.pending_attack.get("targets_self"):
                apply_effect(self.pending_attack, self.player_status, self.player_status, messages,
                             target_name=f"Your {self.selected_pyramun}")

            if self.enemy_hp == 0:
                messages.append(f"Enemy {self.enemy_pyramun} fainted!")
                self._enqueue(*messages)
                self.message_phase = 2
                self._show_next(timer=120)
                return None

            self._enqueue(*messages)
            self.message_phase = 8
            self._show_next()
            return None

        elif phase == 8:
            chip, chip_msgs = self.player_status.resolve_end_of_turn(self.player_stats["hp"], f"Your {self.selected_pyramun}")
            if chip > 0:
                self.player_hp = max(0, self.player_hp - chip)
                if self.player_hp == 0:
                    chip_msgs.append(f"Your {self.selected_pyramun} fainted!")
                    self._enqueue(*chip_msgs)
                    self.message_phase = 2
                    self._show_next(timer=120)
                    return None
                self._enqueue(*chip_msgs)
                self._show_next()
            self.message_phase = 1 if self.player_went_first else 9
            self.message_timer = 1
            return None

        elif phase == 9:
            chip, chip_msgs = self.enemy_status.resolve_end_of_turn(self.enemy_stats["hp"], f"Enemy {self.enemy_pyramun}")
            if chip > 0:
                self.enemy_hp = max(0, self.enemy_hp - chip)
                if self.enemy_hp == 0:
                    chip_msgs.append(f"Enemy {self.enemy_pyramun} fainted!")
                    self._enqueue(*chip_msgs)
                    self.message_phase = 2
                    self._show_next(timer=120)
                    return None
                self._enqueue(*chip_msgs)
                self._show_next()
            self.message_phase = 6
            self.message_timer = 1
            return None

        #egg
        elif phase == 3:
            return "BATTLE"

        elif phase == 1:
            self.message_phase = 7
            self.message_timer = 1
            return None

        elif phase == 7:
            if self.enemy_pending_attack is None:
                self._pick_enemy_move()

            move_name = self.enemy_pending_attack["name"]

            if self.enemy_pending_attack.get("wind_up") and not self._wind_up_shown:
                self._wind_up_shown = True
                self.battle_message = f"Enemy {self.enemy_pyramun} is winding up!"
                self.message_phase  = 7
                self.message_timer  = 90
                return None

            self._wind_up_shown = False
            self.battle_message = f"Enemy {self.enemy_pyramun} used {move_name}!"
            self.message_phase  = 4
            self.message_timer  = 90
            return None

        elif phase == 4:
            anim.trigger_attack("enemy_attack")
            self.message_phase = 5
            self.message_timer = 30
            return None

        elif phase == 5:
            if self.enemy_status.flinched:
                self.enemy_status.flinched = False
                if self.player_went_first:
                    self._enqueue(f"Enemy {self.enemy_pyramun} flinched!")
                    self.message_phase = 9
                    if not self._show_next():
                        self.message_timer = 1
                    return None

            can_move, pre_msgs = self.enemy_status.resolve_before_move(f"Enemy {self.enemy_pyramun}")
            if pre_msgs:
                self._enqueue(*pre_msgs)

            if not can_move:
                if pre_msgs and "hurt itself" in "".join(pre_msgs):
                    self.enemy_hp = max(0, self.enemy_hp - max(1, self.enemy_hp // 8))
                    if self.enemy_hp == 0:
                        pre_msgs.append(f"Enemy {self.enemy_pyramun} fainted!")
                        self._enqueue(*pre_msgs)
                        self.message_phase = 2
                        self._show_next(timer=120)
                        return None
                if self.player_went_first:
                    self.message_phase = 9
                    if not self._show_next():
                        self.message_timer = 1
                else:
                    self.message_phase = 0
                    self.battle_message = f"Your {self.selected_pyramun} used {self.pending_attack['name']}!"
                    if not self._show_next():
                        self.message_timer = 90
                return None

            attack = self.enemy_pending_attack
            self.enemy_status.last_move = attack["name"]

            hit_damages, mult = calculate_damage(
                attack,
                self.enemy_stats, self.player_stats,
                self.enemy_status, self.player_status,
                self.selected_pyramun,
            )

            messages = []

            if hit_damages is None:
                messages.append(f"Enemy {self.enemy_pyramun}'s attack missed!")
                self._enqueue(*messages)
                if self.player_went_first:
                    self.message_phase = 9
                    self._show_next()
                else:
                    self.message_phase = 0
                    self.battle_message = f"Your {self.selected_pyramun} used {self.pending_attack['name']}!"
                    self.message_timer = 90
                return None

            total_damage = sum(hit_damages)
            hit_count    = len(hit_damages)

            if hit_count > 1:
                next_after = 9 if self.player_went_first else 0
                self._mh_queue = list(hit_damages)
                self._mh_total = hit_count
                self._mh_side  = "player"
                self._mh_mult  = mult
                self._mh_next  = next_after
                self.message_phase  = 10
                self.message_timer  = 1
                return None

            if total_damage > 0:
                self.player_hp = max(0, self.player_hp - total_damage)
                anim.trigger_blink("player")

                if mult is not None and mult != 1:
                    if   mult == 0: messages.append("It had no effect!")
                    elif mult > 1:  messages.append("It's super effective!")
                    else:           messages.append("It's not very effective...")

            #enemy effects
            if hit_damages is not None and self.player_hp > 0:
                apply_effect(attack, self.player_status, self.enemy_status, messages,
                             target_moves=ATTACKS[self.selected_pyramun],
                             target_name=f"Your {self.selected_pyramun}")

            #self effects
            if attack.get("targets_self"):
                apply_effect(attack, self.enemy_status, self.enemy_status, messages,
                             target_name=f"Enemy {self.enemy_pyramun}")

            if self.player_hp == 0:
                self._enqueue(*messages)
                self._enqueue(f"Your {self.selected_pyramun} fainted!")
                self.message_phase = 2
                self._show_next(timer=120)
                return None

            self._enqueue(*messages)
            if self.player_went_first:
                self.message_phase = 9
                if not self._show_next():
                    self.message_timer = 1
            else:
                self.message_phase = 0
                self.battle_message = f"Your {self.selected_pyramun} used {self.pending_attack['name']}!"
                self.message_timer = 90
            return None

        elif phase == 10:
            if self._mh_queue:
                dmg = self._mh_queue.pop(0)
                hits_so_far = self._mh_total - len(self._mh_queue)
                move_name = (self.pending_attack["name"] if self._mh_side == "enemy"
                             else self.enemy_pending_attack["name"])

                if self._mh_side == "enemy":
                    self.enemy_hp = max(0, self.enemy_hp - dmg)
                    anim.trigger_blink("enemy", duration=25)
                    if self.enemy_hp == 0:
                        self._enqueue(f"Hit {hits_so_far} time{'s' if hits_so_far > 1 else ''}!")
                        self._enqueue(f"Enemy {self.enemy_pyramun} fainted!")
                        self.message_phase = 2
                        self._show_next(timer=240)
                        return None
                else:
                    self.player_hp = max(0, self.player_hp - dmg)
                    anim.trigger_blink("player", duration=25)
                    if self.player_hp == 0:
                        self._enqueue(f"Hit {hits_so_far} time{'s' if hits_so_far > 1 else ''}!")
                        self._enqueue(f"Your {self.selected_pyramun} fainted!")
                        self.message_phase = 2
                        self._show_next(timer=120)
                        return None

                self.battle_message = f"{move_name}!"
                self.message_timer  = 30
                return None

            messages = [f"Hit {self._mh_total} times!"]
            mult = self._mh_mult
            if mult is not None and mult != 1:
                if   mult == 0: messages.append("It had no effect!")
                elif mult > 1:  messages.append("It's super effective!")
                else:           messages.append("It's not very effective...")

            if self._mh_side == "enemy":
                apply_effect(self.pending_attack, self.enemy_status, self.player_status, messages,
                             target_name=f"Enemy {self.enemy_pyramun}")
                if self.pending_attack.get("targets_self"):
                    apply_effect(self.pending_attack, self.player_status, self.player_status, messages,
                                 target_name=f"Your {self.selected_pyramun}")
            else:
                atk = self.enemy_pending_attack
                apply_effect(atk, self.player_status, self.enemy_status, messages,
                             target_name=f"Your {self.selected_pyramun}")
                if atk.get("targets_self"):
                    apply_effect(atk, self.enemy_status, self.enemy_status, messages,
                                 target_name=f"Enemy {self.enemy_pyramun}")

            self._enqueue(*messages)

            if self._mh_next == 0:
                self.message_phase = 0
                self.battle_message = f"Your {self.selected_pyramun} used {self.pending_attack['name']}!"
                self.message_timer = 90
            else:
                self.message_phase = self._mh_next
                if not self._show_next():
                    self.message_timer = 1
            return None

        elif phase == 6:
            return "BATTLE"

        elif phase == 2:
            self.last_fainted = "player" if self.player_hp == 0 else "enemy"
            return "BATTLE_END"

        return None