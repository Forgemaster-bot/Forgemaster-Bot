import Quick_Google
import Quick_Python
import SQL_Lookup
import SQL_Check


# Character commands
def insert_new_character(character_name: str):
    roster = Quick_Google.sheet("Roster")
    print_row = len(roster.col_values(1)) + 1
    character_sheet = SQL_Lookup.character_sheet(character_name)
    levelup = SQL_Check.level_up_check(character_name)

    # split data
    discord_name = SQL_Lookup.player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = SQL_Lookup.character_sum_class_levels(character_name)
    strength = character_sheet.Strength
    dexterity = character_sheet.Dexterity
    constitution = character_sheet.Constitution
    intelligence = character_sheet.Intelligence
    wisdom = character_sheet.Wisdom
    charisma = character_sheet.Charisma
    gold = character_sheet.Gold

    new_character = [discord_name, character_name, race, background, "", "", "", xp, level, levelup,
                     strength, dexterity, constitution, intelligence, wisdom, charisma, gold]
    roster.insert_row(new_character, print_row)


def update_character(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    character_sheet = SQL_Lookup.character_sheet(character_name)
    levelup = SQL_Check.level_up_check(character_name)

    # split data
    discord_name = SQL_Lookup.player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = SQL_Lookup.character_sum_class_levels(character_name)
    strength = character_sheet.Strength
    dexterity = character_sheet.Dexterity
    constitution = character_sheet.Constitution
    intelligence = character_sheet.Intelligence
    wisdom = character_sheet.Wisdom
    charisma = character_sheet.Charisma
    gold = character_sheet.Gold

    new_character = [discord_name, character_name, race, background, "", "", "", xp, level, levelup,
                     strength, dexterity, constitution, intelligence, wisdom, charisma, gold]
    for col in range(0, 17):
        roster.update_cell(character_row, col+1, new_character[col])


def update_classes(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    class_count = SQL_Lookup.character_count_classes(character_name)
    for class_number in range(1, class_count+1):
            class_detail = SQL_Lookup.character_class_by_order(character_name, class_number)
            roster.update_cell(character_row, class_number+4, "{} {}".format(class_detail[0], class_detail[1]))


# Feats
def update_feat(character_name: str):
    # get google sheet data
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    feat_list = SQL_Lookup.character_feats(character_name)
    feats = Quick_Python.stitch_string(feat_list)
    roster.update_cell(character_row, 18, feats)


# Gold
def update_gold_group(character_list: list):
    roster = Quick_Google.sheet("Roster")
    for character_name in character_list:
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        gold = SQL_Lookup.character_gold(character_name.lstrip())
        roster.update_cell(character_row, 17, gold)


# Items
def update_items(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    item_list = SQL_Lookup.character_inventory(character_name)
    items = Quick_Python.stitch_string(item_list)
    roster.update_cell(character_row, 20, items)


def kill_character(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    reason = c_list[1].lstrip()

    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    character_sheet = roster.row_values(character_row)

    graveyard = Quick_Google.sheet("Graveyard")
    print_row = len(graveyard.col_values(1))+1

    graveyard.insert_row(character_sheet, print_row)
    graveyard.update_cell(print_row, 20, reason)
    roster.delete_row(character_row)

    return "{} died by {}".format(character_name, reason)


# Level up
def update_level(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    level = SQL_Lookup.character_sum_class_levels(character_name)
    level_up = SQL_Check.level_up_check(character_name)
    roster.update_cell(character_row, 9, level)
    roster.update_cell(character_row, 10, level_up)


def update_skill(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    skill_list = SQL_Lookup.character_skills(character_name)
    skills = Quick_Python.stitch_string(skill_list)
    roster.update_cell(character_row, 19, skills)


# XP
def update_xp_group(character_list: list):
    roster = Quick_Google.sheet("Roster")
    for character_name in character_list:
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        xp = SQL_Lookup.character_xp(character_name.lstrip())
        level_up = SQL_Check.level_up_check(character_name.lstrip())

        roster.update_cell(character_row, 8, xp)
        roster.update_cell(character_row, 10, level_up)


def update_character_ability(character_name: str, ability: str):
    roster = Quick_Google.sheet("Roster")
    character_sheet = SQL_Lookup.character_sheet(character_name)
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    if ability == "STR":
        roster.update_cell(character_row, 11, character_sheet.Strength)
    if ability == "DEX":
        roster.update_cell(character_row, 12, character_sheet.Dexterity)
    if ability == "CON":
        roster.update_cell(character_row, 13, character_sheet.Constitution)
    if ability == "INT":
        roster.update_cell(character_row, 14, character_sheet.Intelligence)
    if ability == "WIS":
        roster.update_cell(character_row, 15, character_sheet.Wisdom)
    if ability == "CHA":
        roster.update_cell(character_row, 16, character_sheet.Charisma)


