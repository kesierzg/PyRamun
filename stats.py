import random

BASE_STATS = {
    "Chadmandor": {"hp": 114, "atk": 72, "def": 63, "spd": 85, "spc": 75},
    "Sqqqrtle":   {"hp": 119, "atk": 68, "def": 85, "spd": 63, "spc": 84},
    "Bulwazaur":  {"hp": 120, "atk": 69, "def": 69, "spd": 65, "spc": 85},
    "Pikablu":    {"hp": 110, "atk": 75, "def": 50, "spd": 110, "spc": 65},
    "Pejot":      {"hp": 115, "atk": 65, "def": 60, "spd": 76, "spc": 55},
    "Sandskrew":  {"hp": 125, "atk": 95, "def": 105, "spd": 60, "spc": 45},
    "Psikabra":   {"hp": 110, "atk": 55, "def": 50, "spd": 125, "spc": 115},
}

def generate_stats(name):
    base = BASE_STATS[name]

    return {
        "hp": base["hp"] + random.randint(-6, 6),
        "atk": base["atk"] + random.randint(-6, 6),
        "def": base["def"] + random.randint(-6, 6),
        "spd": base["spd"] + random.randint(-6, 6),
        "spc": base["spc"] + random.randint(-6, 6),
    }