import Quick_Python
import Connections


# Character commands
def insert_new_character(character_name: str):
    roster = Connections.google_sheet("Roster")
    print_row = len(roster.col_values(1)) + 1
    character_sheet = lookup_character_sheet(character_name)
    levelup = check_level_up(character_name)

    # split data
    discord_name = lookup_player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = lookup_character_sum_class_levels(character_name)
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
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    character_sheet = lookup_character_sheet(character_name)
    levelup = check_level_up(character_name)

    # split data
    discord_name = lookup_player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = lookup_character_sum_class_levels(character_name)
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
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    class_count = lookup_character_count_classes(character_name)
    for class_number in range(1, class_count+1):
            class_detail = lookup_character_class_by_order(character_name, class_number)
            roster.update_cell(character_row, class_number+4, "{} {}".format(class_detail[0], class_detail[1]))


# Feats
def update_feat(character_name: str):
    # get google sheet data
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    feat_list = lookup_character_feats(character_name)
    feats = Quick_Python.stitch_string(feat_list)
    roster.update_cell(character_row, 18, feats)


# Gold
def update_gold_group(character_list: list):
    roster = Connections.google_sheet("Roster")
    for character_name in character_list:
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        gold = lookup_character_gold(character_name.lstrip())
        roster.update_cell(character_row, 17, gold)


# Items
def update_items(character_name: str):
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    item_list = lookup_character_inventory(character_name)
    items = Quick_Python.stitch_string(item_list)
    roster.update_cell(character_row, 20, items)


def kill_character(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    reason = c_list[1].lstrip()

    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    character_sheet = roster.row_values(character_row)

    graveyard = Connections.google_sheet("Graveyard")
    print_row = len(graveyard.col_values(1))+1

    graveyard.insert_row(character_sheet, print_row)
    graveyard.update_cell(print_row, 20, reason)
    roster.delete_row(character_row)

    return "{} died by {}".format(character_name, reason)


# Level up
def update_level(character_name: str):
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    level = lookup_character_sum_class_levels(character_name)
    level_up = check_level_up(character_name)
    roster.update_cell(character_row, 9, level)
    roster.update_cell(character_row, 10, level_up)


def update_skill(character_name: str):
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    skill_list = lookup_character_skills(character_name)
    skills = Quick_Python.stitch_string(skill_list)
    roster.update_cell(character_row, 19, skills)


# XP
def update_xp_group(character_list: list):
    roster = Connections.google_sheet("Roster")
    for character_name in character_list:
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        xp = lookup_character_xp(character_name.lstrip())
        level_up = check_level_up(character_name.lstrip())

        roster.update_cell(character_row, 8, xp)
        roster.update_cell(character_row, 10, level_up)


def update_character_ability(character_name: str, ability: str):
    roster = Connections.google_sheet("Roster")
    character_sheet = lookup_character_sheet(character_name)
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


def lookup_character_sheet(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    return cursor.fetchone()


def lookup_player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def lookup_character_sum_class_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def lookup_character_count_classes(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select Count(*) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def lookup_character_class_by_order(character_name: str, order: int):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Class where Character='{}' and Number = '{}'".format(character_name, order)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Class, class_lookup.Level


def lookup_character_feats(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Feats where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    feats = []
    for row in rows:
        feats.append(row.Feat)
    return feats


def lookup_character_gold(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def lookup_character_inventory(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character='{}' order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def lookup_character_skills(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Skills where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        if row.Proficiency == 1:
            skills.append(row.Skill)
        else:
            skills.append(row.Skill + " (D)")
    return skills


def lookup_character_xp(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def check_level_up(character_name: str):
    character_level = lookup_character_sum_class_levels(character_name)
    character_xp = lookup_character_xp(character_name)
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return "Yes"
    return "No"
