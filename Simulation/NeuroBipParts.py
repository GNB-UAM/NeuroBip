NBHips = {
    "controller": {
        "noCollideGroup" : -1,
        "coords": [(0, 38), (50, 38), (50, 42), (0, 42)],
        "weight": 10
    },
    "base": {
        "noCollideGroup" : -1,
        "coords": [(0, 33), (50, 33), (50, 38), (0, 38)],
        "weight": 31.2 - 2 * 7*(31.2 / 36) #total - 2 * 7 motor pla
    },
    "motor": {
        "noCollideGroup" : -1,
        "coords": [(16.5, 0), (33.5, 0), (33.5, 33), (16.5, 33)],
        "weight": 13.2 + 7*(31.2 / 36 ) # + 7 g motor pla
    }
}

NBFemur = {
    "femur": {
        "noCollideGroup" : -1,
        "coords": [(0, 33), (21, 33), (21, 78.8), (0, 78.8)],
        "weight": 13.2 - 8*(13.2 / 14) #total - 8 motor pla
    },
    "motor": {
        "noCollideGroup" : -1,
        "coords": [(2, 0), (19, 0), (19, 33), (2, 33)],
        "weight": 13.2 + 8*(13.2 / 14) # + 8 g pla
    }
}

NBFoot = {
    "tibia": {
        "noCollideGroup" : -1,
        "coords": [(3, 21), (24, 21), (24, 67.7), (3, 67.7)],
        "weight": 16.2 - (5 + 9) * (16.2 / 19) #total - 5 battery pla - 9 sole pla
    },
    "battery": {
        "noCollideGroup" : -1,
        "coords": [(0, 4), (44.9, 4), (44.9, 21), (0, 21)],
        "weight": 31.2 + 5 * (16.2 / 19) # + 5 g pla cura
    },
    "sole": {
        "noCollideGroup" : -1,
        "coords": [(0, 0), (45, 0), (45, 4), (0, 4)],
        "weight": 9 * (16.2 / 19) # 9 g sole cura
    }
}