first_row = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
second_row = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]

types = [
    "Металлокерамика",
    "Диоксид циркония",
    "Полный сьемный протез",
    "Частичный сьемный протез",
    "Цельнолитая коронка из кхс",
    "Штампованная коронка",
    "Телескопическая коронка",
    "Бюгельный протез на аттачменах",
    "Другое"
]
color_letter = ["A", "B", "C", "D"]
color_number = ["1", "2", "3", "3.5", "4"]
tooth_priority = ["gutta", "tab","fiberglass","implant", "seal", "crown", "periodont", "bracket", "tooth"]

tooth_data = {
    36: {"x": 459, "name": "molar", "type": "left_lower"},
    37: {"x": 505, "name": "molar", "type": "left_lower"},
    38: {"x": 555, "name": "molar", "type": "left_lower"},
    46: {"x": 120, "name": "molar", "type": "right_lower"},
    47: {"x": 75, "name": "molar", "type": "right_lower"},
    48: {"x": 24, "name": "molar", "type": "right_lower"},

    35: {"x": 418, "name": "premolar", "type": "lower"},
    34: {"x": 388, "name": "premolar", "type": "lower"},
    33: {"x": 353, "name": "premolar", "type": "lower"},
    45: {"x": 158, "name": "premolar", "type": "lower"},
    44: {"x": 188, "name": "premolar", "type": "lower"},
    43: {"x": 222, "name": "premolar", "type": "lower"},

    42: {"x": 253, "name": "incisor", "type": "lower_center"},
    41: {"x": 277, "name": "incisor", "type": "lower_center"},
    32: {"x": 323, "name": "incisor", "type": "lower_center"},
    31: {"x": 300, "name": "incisor", "type": "lower_center"},

    26: {"x": 459, "name": "molar", "type": "left_upper"},
    27: {"x": 504, "name": "molar", "type": "left_upper"},
    28: {"x": 555, "name": "molar", "type": "left_upper"},
    16: {"x": 120, "name": "molar", "type": "right_upper"},
    17: {"x": 75, "name": "molar", "type": "right_upper"},
    18: {"x": 24, "name": "molar", "type": "right_upper"},

    25: {"x": 421, "name": "premolar", "type": "upper"},
    24: {"x": 391, "name": "premolar", "type": "upper"},
    23: {"x": 361, "name": "premolar", "type": "upper"},
    22: {"x": 335, "name": "incisor", "type": "upper_center"},
    21: {"x": 306, "name": "incisor", "type": "upper_center"},
    15: {"x": 155, "name": "premolar", "type": "upper"},
    14: {"x": 184, "name": "premolar", "type": "upper"},
    13: {"x": 214, "name": "premolar", "type": "upper"},
    12: {"x": 242, "name": "incisor", "type": "upper_center"},
    11: {"x": 269, "name": "incisor", "type": "upper_center"},

}

image_data = {
    "crown": {
        "right_lower":
            {
                "delta": -10,
                "y": 307,
                "width": 41,
                "height": 33
            },
        "left_lower": {
            "delta": -10,
            "y": 307,
            "width": 41,
            "height": 33
        },
        "lower": {
            "delta": 0,
            "y": 306,
            "width": 26,
            "height": 30
        },
        "lower_center": {
            "delta": 3,
            "y": 305,
            "width": 19,
            "height": 31
        },
        "right_upper":
            {
                "delta": -10,
                "y": 263,
                "width": 41,
                "height": 33
            },
        "left_upper": {
            "delta": -10,
            "y": 263,
            "width": 41,
            "height": 33
        },
        "upper": {
            "delta": -1,
            "y": 261,
            "width": 28,
            "height": 36
        },
        "upper_center": {
            "delta": -1,
            "y": 266,
            "width": 27,
            "height": 35
        },
    },
    "bracket": {
        "right_lower":
            {
                "delta": -5,
                "y": 318,
                "width": 33,
                "height": 15
            },
        "left_lower": {
            "delta": -6,
            "y": 318,
            "width": 33,
            "height": 15
        },
        "lower": {
            "delta": -1,
            "y": 317,
            "width": 26,
            "height": 13
        },
        "lower_center": {
            "delta": 5,
            "y": 317,
            "width": 16,
            "height": 11
        },
        "right_upper":
            {
                "delta": -5,
                "y": 273,
                "width": 33,
                "height": 15
            },
        "left_upper": {
            "delta": -5,
            "y": 273,
            "width": 33,
            "height": 15
        },
        "upper": {
            "delta": -1,
            "y": 274,
            "width": 26,
            "height": 16
        },
        "upper_center": {
            "delta": -1,
            "y": 274,
            "width": 26,
            "height": 16
        },
    },
    "remove": {
        "right_lower": {
            "delta": -2,
            "y": 320,
            "width": 28,
            "height": 45
        },
        "left_lower": {
            "delta": -3,
            "y": 320,
            "width": 28,
            "height": 45
        },
        "lower": {
            "delta": 0,
            "y": 320,
            "width": 28,
            "height": 45
        },
        "lower_center": {
            "delta": 3,
            "y": 320,
            "width": 20,
            "height": 45
        },
        "right_upper": {
            "delta": -2,
            "y": 240,
            "width": 28,
            "height": 45
        },
        "left_upper": {
            "delta": -3,
            "y": 240,
            "width": 28,
            "height": 45
        },
        "upper": {
            "delta": -1,
            "y": 240,
            "width": 28,
            "height": 45
        },
        "upper_center": {
            "delta": 2,
            "y": 240,
            "width": 22,
            "height": 45
        },
    },
    "caries": {
        "right_lower": {
            "delta": 5,
            "y": 317,
            "width": 18,
            "height": 18
        },
        "left_lower": {
            "delta": 4,
            "y": 317,
            "width": 18,
            "height": 18
        },
        "lower": {
            "delta": 5,
            "y": 313,
            "width": 18,
            "height": 18
        },
        "lower_center": {
            "delta": 7,
            "y": 310,
            "width": 13,
            "height": 18
        },
        "right_upper": {
            "delta": 5,
            "y": 271,
            "width": 18,
            "height": 18
        },
        "left_upper": {
            "delta": 4,
            "y": 271,
            "width": 18,
            "height": 18
        },
        "upper": {
            "delta": 5,
            "y": 268,
            "width": 18,
            "height": 18
        },
        "upper_center": {
            "delta": 4,
            "y": 272,
            "width": 18,
            "height": 18
        },
    },
    "periodont": {
        "right_lower": {
            "delta": 5,
            "y": 374,
            "width": 14,
            "height": 13
        },
        "left_lower": {
            "delta": 4,
            "y": 374,
            "width": 14,
            "height": 13
        },
        "lower": {
            "delta": 5,
            "y": 374,
            "width": 14,
            "height": 13
        },
        "lower_center": {
            "delta": 7,
            "y": 374,
            "width": 14,
            "height": 13
        },
        "right_upper": {
            "delta": 5,
            "y": 216,
            "width": 14,
            "height": 13
        },
        "left_upper": {
            "delta": 4,
            "y": 216,
            "width": 14,
            "height": 13
        },
        "upper": {
            "delta": 5,
            "y": 213,
            "width": 14,
            "height": 13
        },
        "upper_center": {
            "delta": 4,
            "y": 213,
            "width": 14,
            "height": 13
        },
    },
    "tab": {
        "right_lower":
            {
                "delta": -1,
                "y": 316,
                "width": 28,
                "height": 37
            },
        "left_lower": {
            "delta": -4,
            "y": 316,
            "width": 28,
            "height": 37
        },
        "lower": {
            "delta": 5,
            "y": 319,
            "width": 18,
            "height": 41
        },
        "lower_center": {
            "delta": 7,
            "y": 319,
            "width": 12,
            "height": 41
        },
        "right_upper":
            {
                "delta": -2,
                "y": 248,
                "width": 28,
                "height": 37
            },
        "left_upper": {
            "delta": -2,
            "y": 248,
            "width": 28,
            "height": 37
        },
        "upper": {
            "delta": 4,
            "y": 237,
            "width": 18,
            "height": 41
        },
        "upper_center": {
            "delta": 4,
            "y": 237,
            "width": 18,
            "height": 41
        },
    },

    "implant": {
        "right_lower":
            {
                "delta": -3,
                "y": 336,
                "width": 32,
                "height": 48
            },
        "left_lower": {
            "delta": -3,
            "y": 336,
            "width": 32,
            "height": 48
        },
        "lower": {
            "delta": 4,
            "y": 335,
            "width": 20,
            "height": 44
        },
        "lower_center": {
            "delta": 5,
            "y": 335,
            "width": 17,
            "height": 46
        },
        "right_upper":
            {
                "delta": -5,
                "y": 216,
                "width": 32,
                "height": 53
            },
        "left_upper": {
            "delta": -5,
            "y": 216,
            "width": 32,
            "height": 53
        },
        "upper": {
            "delta": 4,
            "y": 220,
            "width": 20,
            "height": 44
        },
        "upper_center": {
            "delta": 4,
            "y": 220,
            "width": 20,
            "height": 44
        },
    },
    "fiberglass": {
        "right_lower":
            {
                "delta": 4,
                "y": 314,
                "width": 26,
                "height": 48
            },
        "left_lower": {
            "delta": -7,
            "y": 314,
            "width": 26,
            "height": 48
        },
        "lower": {
            "delta": 0,
            "y": 312,
            "width": 20,
            "height": 50
        },
        "lower_center": {
            "delta": 6,
            "y": 312,
            "width": 13,
            "height": 50
        },
        "right_upper":
            {
                "delta": 5,
                "y": 235,
                "width": 25,
                "height": 57
            },
        "left_upper": {
            "delta": -5,
            "y": 237,
            "width": 25,
            "height": 57
        },
        "upper": {
            "delta": 4,
            "y": 237,
            "width": 23,
            "height": 57
        },
        "upper_center": {
            "delta": 2,
            "y": 237,
            "width": 23,
            "height": 57
        },
    },
    "seal": {
        "right_lower":
            {
                "delta": -9,
                "y": 308,
                "width": 45,
                "height": 20
            },
        "left_lower": {
            "delta": -11,
            "y": 308,
            "width": 45,
            "height": 20
        },
        "lower": {
            "delta": 0,
            "y": 312,
            "width": 20,
            "height": 50
        },
        "lower_center": {
            "delta": 6,
            "y": 312,
            "width": 13,
            "height": 50
        },
        "right_upper":
            {
                "delta": -10,
                "y": 278,
                "width": 45,
                "height": 20
            },
        "left_upper": {
            "delta": -11,
            "y": 278,
            "width": 45,
            "height": 20
        },
        "upper": {
            "delta": -10,
            "y": 275,
            "width": 40,
            "height": 18
        },
        "upper_center": {
            "delta": 2,
            "y": 237,
            "width": 23,
            "height": 57
        },
    },
    "gutta": {
        "lower":
            {
                "delta": 10,
                "y": 337,
                "width": 7,
                "height": 41
            },
        "left_lower":
            {
                "delta": -2,
                "y": 336,
                "width": 29,
                "height": 39
            },
        "right_lower":
            {
                "delta": -5,
                "y": 336,
                "width": 29,
                "height": 39
            },
        "lower_center": {
            "delta": 11,
            "y": 336,
            "width": 4,
            "height": 41
        },
        "upper":
            {
                "delta": 10,
                "y": 221,
                "width": 7,
                "height": 40
            },
        "left_upper":
            {
                "delta": -2,
                "y": 229,
                "width": 29,
                "height": 39
            },
        "right_upper":
            {
                "delta": -5,
                "y": 229,
                "width": 29,
                "height": 39
            },
        "upper_center": {
            "delta": 11,
            "y": 221,
            "width": 4,
            "height": 40
        },
    }

}
