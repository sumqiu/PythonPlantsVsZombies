__author__ = 'marble_xu'

from ... import constants as c

# Panel layout constants
PANEL_Y_START = 87
PANEL_X_START = 22
PANEL_Y_INTERNAL = 74
PANEL_X_INTERNAL = 53
CARD_LIST_NUM = 8

# Single source of truth for card ↔ plant mapping, sun cost and cooldown.
# Each entry's list index IS the card's name_index used throughout the codebase.
CARD_CONFIG = [
    # idx  card image name             plant/entity name       sun   cd (ms)
    {"card": c.CARD_SUNFLOWER,          "plant": c.SUNFLOWER,          "sun":  50, "cd":  7500},  # 0
    {"card": c.CARD_PEASHOOTER,         "plant": c.PEASHOOTER,         "sun": 100, "cd":  7500},  # 1
    {"card": c.CARD_SNOWPEASHOOTER,     "plant": c.SNOWPEASHOOTER,     "sun": 175, "cd":  7500},  # 2
    {"card": c.CARD_WALLNUT,            "plant": c.WALLNUT,            "sun":  50, "cd": 30000},  # 3
    {"card": c.CARD_CHERRYBOMB,         "plant": c.CHERRYBOMB,         "sun": 150, "cd": 50000},  # 4
    {"card": c.CARD_THREEPEASHOOTER,    "plant": c.THREEPEASHOOTER,    "sun": 325, "cd":  7500},  # 5
    {"card": c.CARD_REPEATERPEA,        "plant": c.REPEATERPEA,        "sun": 200, "cd":  7500},  # 6
    {"card": c.CARD_CHOMPER,            "plant": c.CHOMPER,            "sun": 150, "cd":  7500},  # 7
    {"card": c.CARD_PUFFSHROOM,         "plant": c.PUFFSHROOM,         "sun":   0, "cd":  7500},  # 8
    {"card": c.CARD_POTATOMINE,         "plant": c.POTATOMINE,         "sun":  25, "cd": 30000},  # 9
    {"card": c.CARD_SQUASH,             "plant": c.SQUASH,             "sun":  50, "cd": 30000},  # 10
    {"card": c.CARD_SPIKEWEED,          "plant": c.SPIKEWEED,          "sun": 100, "cd":  7500},  # 11
    {"card": c.CARD_JALAPENO,           "plant": c.JALAPENO,           "sun": 125, "cd": 50000},  # 12
    {"card": c.CARD_SCAREDYSHROOM,      "plant": c.SCAREDYSHROOM,      "sun":  25, "cd":  7500},  # 13
    {"card": c.CARD_SUNSHROOM,          "plant": c.SUNSHROOM,          "sun":  25, "cd":  7500},  # 14
    {"card": c.CARD_ICESHROOM,          "plant": c.ICESHROOM,          "sun":  75, "cd": 50000},  # 15
    {"card": c.CARD_HYPNOSHROOM,        "plant": c.HYPNOSHROOM,        "sun":  75, "cd": 30000},  # 16
    {"card": c.CARD_WALLNUT,            "plant": c.WALLNUTBOWLING,     "sun":   0, "cd":     0},  # 17
    {"card": c.CARD_REDWALLNUT,         "plant": c.REDWALLNUTBOWLING,  "sun":   0, "cd":     0},  # 18
    {"card": c.CARD_BUCKETHEAD_ZOMBIE,  "plant": c.BUCKETHEAD_ZOMBIE,  "sun": 150, "cd": 20000},  # 19
    {"card": c.CARD_CONEHEAD_ZOMBIE,    "plant": c.CONEHEAD_ZOMBIE,    "sun":  75, "cd": 15000},  # 20
    {"card": c.CARD_NORMAL_ZOMBIE,      "plant": c.NORMAL_ZOMBIE,      "sun":  50, "cd": 10000},  # 21
]

all_card_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21]

# Zombie card indices
ZOMBIE_CARD_INDEX_START = 19
ZOMBIE_CARD_BUCKETHEAD = 19
ZOMBIE_CARD_CONEHEAD = 20
ZOMBIE_CARD_NORMAL = 21
