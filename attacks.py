TYPE_EFFECTIVENESS = {
    "fire":     {"grass": 2, "water": 0.5, "fire": 0.5, "rock": 0.5},
    "water":    {"fire": 2, "grass": 0.5, "water": 0.5, "rock": 2},
    "grass":    {"water": 2, "fire": 0.5, "grass": 0.5, "rock": 2},
    "electric": {"water": 2, "grass": 0.5, "electric": 0.5, "ground": 0},
    "ice":      {"grass": 2, "ground": 2, "flying": 2, "dragon": 2, "fire": 0.5},
    "fighting": {"normal": 2, "rock": 2, "ice": 2, "ghost": 0},
    "poison":   {"grass": 2, "poison": 0.5, "ground": 0.5},
    "ground":   {"fire": 2, "electric": 2, "poison": 2, "flying": 0},
    "flying":   {"grass": 2, "fighting": 2, "electric": 0.5},
    "psychic":  {"fighting": 2, "poison": 2, "dark": 0},
    "bug":      {"grass": 2, "psychic": 2, "fire": 0.5},
    "rock":     {"fire": 2, "flying": 2, "ice": 2},
    "ghost":    {"ghost": 2, "normal": 0},
    "dragon":   {"dragon": 2},
    "dark":     {"psychic": 2, "ghost": 2},
    "steel":    {"ice": 2, "rock": 2, "fire": 0.5},
}

PYRAMUN_TYPES = {
    "Chadmandor": "fire",
    "Sqqqrtle":   "water",
    "Bulwazaur":  "grass",
    "Pikablu":    "electric",
    "Pejot":      "flying",
    "Sandskrew":  "ground",
    "Psikabra":   "psychic",
}

TACKLE = {
    "name": "TACKLE",
    "power": 35,
    "accuracy": 95,
    "type": "normal",
    "category": "physical",
    "weight": 0
}

#Chadmandor

EMBER = {
    "name": "EMBER",
    "power": 40,
    "accuracy": 100,
    "type": "fire",
    "category": "special",
    "effect": "burn",
    "effect_chance": 10,
    "weight": 0
}

SLASH = {
    "name": "SLASH",
    "power": 70,
    "accuracy": 100,
    "type": "normal",
    "category": "physical",
    "weight": 0
}

DRAGONRAGE = {
    "name": "DRAGONRAGE",
    "label": "DRGNRAGE",
    "power": 0,
    "accuracy": 80,
    "fixed_damage": 40,
    "type": "dragon",
    "category": "special",
    "weight": 0
}

SCARYFACE = {
    "name": "SCARYFACE",
    "power": 0,
    "accuracy": 90,
    "type": "normal",
    "category": "status",
    "effect": "lower_spd",
    "effect_value": 2,
    "weight": 1
}

#Sqqqrtle

WATERGUN = {
    "name": "WATERGUN",
    "power": 40,
    "accuracy": 95,
    "type": "water",
    "category": "special",
    "weight": 0
}

BITE = {
    "name": "BITE",
    "power": 60,
    "accuracy": 100,
    "type": "dark",
    "category": "special",
    "effect": "flinch",
    "effect_chance": 30,
    "weight": 0
}

BLIZZARD = {
    "name": "BLIZZARD",
    "power": 90,
    "accuracy": 70,
    "type": "ice",
    "category": "special",
    "effect": "freeze",
    "effect_chance": 10,
    "weight": 0
}

SWAGGER = {
    "name": "SWAGGER",
    "power": 0,
    "accuracy": 90,
    "type": "normal",
    "category": "status",
    "effect": "swagger",
    "effect_value": 2,
    "weight": 1
}

#Bulwazaur

RAZORLEAF = {
    "name": "RAZORLEAF",
    "power": 55,
    "accuracy": 95,
    "type": "grass",
    "category": "special",
    "weight": 0
}

POISONPOWDER = {
    "name": "POISONPOWDER",
    "label": "PSNPWDR",
    "power": 0,
    "accuracy": 75,
    "type": "poison",
    "category": "status",
    "effect": "poison",
    "weight": 0
}

HEADBUTT = {
    "name": "HEADBUTT",
    "power": 70,
    "accuracy": 100,
    "type": "normal",
    "category": "physical",
    "effect": "flinch",
    "effect_chance": 30,
    "weight": 0
}

GROWTH = {
    "name": "GROWTH",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "status",
    "effect": "raise_spc",
    "effect_value": 1,
    "targets_self": True,
    "weight": 1
}

#Pikablu

THUNDERBOLT = {
    "name": "THUNDERBOLT",
    "label": "THNBOLT",
    "power": 95,
    "accuracy": 100,
    "type": "electric",
    "category": "physical",
    "effect": "paralysis",
    "effect_chance": 10,
    "weight": 0
}

QUICKATTACK = {
    "name": "QUICKATTACK",
    "label": "QUICKATTK",
    "power": 40,
    "accuracy": 100,
    "type": "normal",
    "category": "physical",
    "priority": 1,
    "weight": 0
}

THUNDERWAVE = {
    "name": "THUNDERWAVE",
    "label": "THNWAVE",
    "power": 0,
    "accuracy": 100,
    "type": "electric",
    "category": "status",
    "effect": "paralysis",
    "weight": 0
}

GROWL = {
    "name": "GROWL",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "status",
    "effect": "lower_atk",
    "effect_value": 1,
    "weight": 1
}

#Pejot

FLY = {
    "name": "FLY",
    "power": 70,
    "accuracy": 95,
    "type": "flying",
    "category": "physical",
    "wind_up": True,
    "weight": 0
}

WINGATTACK = {
    "name": "WINGATTACK",
    "label": "WINGATK",
    "power": 60,
    "accuracy": 100,
    "type": "flying",
    "category": "physical",
    "weight": 0
}

DOUBLETEAM = {
    "name": "DOUBLETEAM",
    "label": "DBLTEAM",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "status",
    "effect": "raise_eva",
    "effect_value": 1,
    "targets_self": True,
    "weight": 1

}

#Sandskrew

FURYSWIPES = {
    "name": "FURYSWIPES",
    "label": "FURYSWPS",
    "power": 18,
    "accuracy": 80,
    "type": "normal",
    "category": "physical",
    "hits": (2, 5),
    "weight": 0
}

SWIFT = {
    "name": "SWIFT",
    "power": 60,
    "accuracy": 100,
    "type": "normal",
    "category": "physical",
    "never_misses": True,
    "weight": 0
}

TOXIC = {
    "name": "TOXIC",
    "power": 0,
    "accuracy": 85,
    "type": "poison",
    "category": "status",
    "effect": "bad_poison",
    "weight": 0
}

#Psikabra

PSYBEAM = {
    "name": "PSYBEAM",
    "power": 65,
    "accuracy": 100,
    "type": "psychic",
    "category": "special",
    "effect": "confusion",
    "effect_chance": 10,
    "weight": 0
}

CONFUSION = {
    "name": "CONFUSION",
    "power": 50,
    "accuracy": 100,
    "type": "psychic",
    "category": "special",
    "effect": "confusion",
    "effect_chance": 10,
    "weight": 0
}

KINESIS = {
    "name": "KINESIS",
    "power": 0,
    "accuracy": 80,
    "type": "psychic",
    "category": "status",
    "effect": "lower_acc",
    "effect_value": 1,
    "weight": 1
}

DISABLE = {
    "name": "DISABLE",
    "power": 0,
    "accuracy": 55,
    "type": "normal",
    "category": "status",
    "effect": "disable",
    "weight": 1
}

ATTACKS = {
    "Chadmandor": [EMBER, SLASH, DRAGONRAGE, SCARYFACE],
    "Sqqqrtle":   [WATERGUN, BITE, BLIZZARD, SWAGGER],
    "Bulwazaur":  [RAZORLEAF, POISONPOWDER, HEADBUTT, GROWTH],
    "Pikablu":    [THUNDERBOLT, QUICKATTACK, THUNDERWAVE, GROWL],
    "Pejot":      [FLY, QUICKATTACK, WINGATTACK, DOUBLETEAM],
    "Sandskrew":  [FURYSWIPES, SWIFT, TOXIC, TACKLE],
    "Psikabra":   [PSYBEAM, CONFUSION, KINESIS, DISABLE],
}

def get_multiplier(attack_type, defender_type):
    return TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1)
