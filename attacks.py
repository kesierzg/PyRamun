TYPES = [
    "normal", "fire", "water", "grass", "electric", "ice",
    "fighting", "poison", "ground", "flying", "psychic",
    "bug", "rock", "ghost", "dragon", "dark", "steel"
]

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
    "category": "physical"
}

##chadmander

EMBER = {
    "name": "EMBER",
    "power": 40,
    "accuracy": 100,
    "type": "fire",
    "category": "special"
}

SLASH = {
    "name": "SLASH",
    "power": 70,
    "accuracy": 100,
    "type": "normal",
    "category": "physical"
}

SCARYFACE = {
    "name": "SCARYFACE",
    "power": 0,
    "accuracy": 90,
    "type": "normal",
    "category": "physical",
    "effect": "lower_speed",
    "effect_value": 2
}

DRAGONRAGE = {
    "name": "DRAGONRAGE",
    "power": 0,
    "accuracy": 80,
    "fixed_damage": 40,
    "type": "dragon",
    "category": "special"
}

##sqqrtle

WATERGUN = {
    "name": "WATERGUN",
    "power": 40,
    "accuracy": 95,
    "type": "water",
    "category": "special"
}

BITE = {
    "name": "BITE",
    "power": 60,
    "accuracy": 100,
    "type": "dark",
    "category": "special"
}

BLIZZARD = {
    "name": "BLIZZARD",
    "power": 90,
    "accuracy": 70,
    "type": "ice",
    "category": "special"##,
    ##"effect": "lower_speed",
    ##"effect_chance": 10
}

SWAGGER = {
    "name": "SWAGGER",
    "power": 0,
    "accuracy": 90,
    "type": "normal",
    "category": "physical"
    ##"effect": "confuse" + "raise_attack",
    ##"effect_value": 1
}

##bulwazaur

RAZORLEAF = {
    "name": "RAZORLEAF",
    "power": 55,
    "accuracy": 95,
    "type": "grass",
    "category": "special"
}

POISONPOWDER = {
    "name": "POISONPOWDER",
    "power": 0,
    "accuracy": 75,
    "type": "poison",
    "category": "physical"
    ##"effect": "posion",
}

HEADBUTT = {
    "name": "HEADBUTT",
    "power": 70,
    "accuracy": 100,
    "type": "normal",
    "category": "physical"
}

GROWTH = {
    "name": "GROWTH",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "physical",
    ##"effect": "higher_special"
}

##pikablu

THUNDERBOLT = {
    "name": "THUNDERBOLT",
    "power": 95,
    "accuracy": 100,
    "type": "electric",
    "category": "physical"
}

QUICKATTACK = {
    "name": "QUICKATTK",
    "power": 40,
    "accuracy": 100, ##inf?
    "type": "normal",
    "category": "physical"##,
    ##priority: 1
}

THUNDERWAVE = {
    "name": "THUNDERWAVE",
    "power": 0,
    "accuracy": 100,
    "type": "electric",
    "category": "special",
    "effect": "paralyze"
}

GROWL = {
    "name": "GROWL",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "physical"##,
    ##"effect": "lower_attack",
    ##"effect_value": 1
}

##pejot

FLY = {
    "name": "FLY",
    "power": 70,
    "accuracy": 95,
    "type": "flying",
    "category": "physical"
    ##ogarnac turn
}

WINGATTACK = {
    "name": "WINGATTACK",
    "power": 60,
    "accuracy": 100,
    "type": "flying",
    "category": "physical"
}

DOUBLETEAM = {
    "name": "DOUBLETEAM",
    "power": 0,
    "accuracy": 100,
    "type": "normal",
    "category": "physical"##,
    ##"effect": "higher_evasiveness",
    ##"effect_value": 1
}

##sandskrew

FURYSWIPES = {
    "name": "FURYSWIPES",
    "power": 18,
    "accuracy": 80,
    "type": "normal",
    "category": "physical"
    ##hits: rand(2-5)
}

SWIFT = {
    "name": "SWIFT",
    "power": 60,
    "accuracy": 100, ##inf?
    "type": "normal",
    "category": "physical"
}

TOXIC = {
    "name": "TOXIC",
    "power": 0,
    "accuracy": 85,
    "type": "poison",
    "category": "physical"
    ##"effect": "poison"
}

##psikabra

PSYBEAM = {
    "name": "PSYBEAM",
    "power": 65,
    "accuracy": 100,
    "type": "psychic",
    "category": "special"
}

CONFUSION = {
    "name": "CONFUSION",
    "power": 50,
    "accuracy": 100,
    "type": "psychic",
    "category": "special"
    ##"effect": "confusion",
    ##"effect_chance": 10
}

KINESIS = {
    "name": "KINESIS",
    "power": 0,
    "accuracy": 80,
    "type": "psychic",
    "category": "special"
    ##"effect": "lower_accuracy",
    ##"effect_value": 1
}

DISABLE = {
    "name": "DISABLE",
    "power": 0,
    "accuracy": 55,
    "type": "normal",
    "category": "physical"
    ##affects: rand(1-8)
}


##ENDURE??
##DIG

ATTACKS = {
    "Chadmandor": [EMBER, SLASH, SCARYFACE, DRAGONRAGE],
    "Sqqqrtle": [WATERGUN, BITE, BLIZZARD, SWAGGER],
    "Bulwazaur": [RAZORLEAF, POISONPOWDER, HEADBUTT, GROWTH],
    "Pikablu": [THUNDERBOLT, QUICKATTACK, THUNDERWAVE, GROWL],
    "Pejot": [FLY, QUICKATTACK, WINGATTACK, DOUBLETEAM],
    "Sandskrew": [FURYSWIPES, SWIFT, TOXIC, TACKLE],
    "Psikabra": [PSYBEAM, CONFUSION, KINESIS, DISABLE]
}

def get_multiplier(attack_type, defender_type):
    return TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1)