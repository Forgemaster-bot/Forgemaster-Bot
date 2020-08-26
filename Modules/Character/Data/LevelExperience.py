total_xp_needed_for_next_level = {
    1: 300,
    2: 900,
    3: 2700,
    4: 6500,
    5: 14000,
    6: 23000,
    7: 34000,
    8: 48000,
    9: 64000,
    10: 85000,
    11: 100000,
    12: 120000,
    13: 140000,
    14: 165000,
    15: 195000,
    16: 225000,
    17: 265000,
    18: 305000,
    19: 355000,
    20: None
}

xp_gap_to_next_level = {
    1: 300,
    2: 600,
    3: 1800,
    4: 3800,
    5: 7500,
    6: 9000,
    7: 11000,
    8: 14000,
    9: 16000,
    10: 21000,
    11: 15000,
    12: 20000,
    13: 20000,
    14: 25000,
    15: 30000,
    16: 30000,
    17: 40000,
    18: 50000,
    19: 50000,
    20: None
}


def can_level_up(current_level: int, total_xp: int):
    xp_needed = total_xp_needed_for_next_level[current_level]
    return (total_xp >= xp_needed) if xp_needed else None


def get_log_xp(current_level: int):
    xp_gap = xp_gap_to_next_level[current_level]
    return (xp_gap / 20) if xp_gap else 0