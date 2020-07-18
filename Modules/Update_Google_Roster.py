import Quick_Python
import Connections


# Character commands
def insert_new_character(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    print_row = len(roster.col_values(1)) + 1
    character_sheet = lookup_character_sheet(character_id)
    levelup = check_level_up(character_id)

    # split data
    discord_name = lookup_player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = lookup_character_sum_class_levels(character_id)
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


def update_character(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    if character_row == 0:
        character_row = len(roster.col_values(1)) + 1
        roster.update_cell(character_row, 2, character_name)
    character_sheet = lookup_character_sheet(character_id)
    levelup = check_level_up(character_id)

    # split data
    discord_name = lookup_player_name_by_id(character_sheet.Discord_ID)
    race = character_sheet.Race
    background = character_sheet.Background
    xp = character_sheet.XP
    level = lookup_character_sum_class_levels(character_id)
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


def update_classes(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    class_count = lookup_character_count_classes(character_id)
    for class_number in range(1, class_count+1):
            class_detail = lookup_character_class_by_order(character_id, class_number)
            roster.update_cell(character_row, class_number+4, "{} {}".format(class_detail[0], class_detail[1]))


# Feats
def update_feat(character_id: str):
    character_name = character_name_by_character_id(character_id)
    # get google sheet data
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    feat_list = lookup_character_feats(character_id)
    feats = Quick_Python.list_to_string(feat_list)
    roster.update_cell(character_row, 18, feats)


# Gold
def update_gold_group(character_id_list: list):
    roster = Connections.google_sheet("Roster")
    for character_id in character_id_list:
        character_name = character_name_by_character_id(character_id)
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        gold = lookup_character_gold(character_id)
        roster.update_cell(character_row, 17, gold)


# Items
def update_items(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    item_list = lookup_character_inventory(character_id)
    items = Quick_Python.list_to_string(item_list)
    roster.update_cell(character_row, 20, items)


def kill_character(character_id: str, reason: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    character_sheet = roster.row_values(character_row)

    graveyard = Connections.google_sheet("Graveyard")
    print_row = len(graveyard.col_values(1))+1

    graveyard.insert_row(character_sheet, print_row)
    graveyard.update_cell(print_row, 20, reason)

    # items
    item_list = lookup_character_inventory(character_id)
    items = Quick_Python.list_to_string(item_list)
    roster.update_cell(character_row, 21, items)

    roster.delete_row(character_row)

    return "{} died by {}".format(character_name, reason)


# Level up
def update_level(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    level = lookup_character_sum_class_levels(character_id)
    level_up = check_level_up(character_id)
    roster.update_cell(character_row, 9, level)
    roster.update_cell(character_row, 10, level_up)


def update_skill(character_id: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    skill_list = lookup_character_skills(character_id)
    skills = Quick_Python.list_to_string(skill_list)
    roster.update_cell(character_row, 19, skills)


# XP
def update_xp_group(character_id_list: list):
    roster = Connections.google_sheet("Roster")
    for character_id in character_id_list:
        character_name = character_name_by_character_id(character_id)
        character_row = Quick_Python.find_character_row(roster.col_values(2), character_name.lstrip())
        xp = lookup_character_xp(character_id.lstrip())
        level_up = check_level_up(character_id.lstrip())

        roster.update_cell(character_row, 8, xp)
        roster.update_cell(character_row, 10, level_up)


def update_character_ability(character_id: str, ability: str):
    character_name = character_name_by_character_id(character_id)
    roster = Connections.google_sheet("Roster")
    character_sheet = lookup_character_sheet(character_id)
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


def lookup_character_sheet(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = ?"
    print("Running query: " + query)
    cursor.execute(query, [character_id])
    return cursor.fetchone()


def lookup_player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= ?"
    print("Running query: " + query)
    cursor.execute(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def lookup_character_sum_class_levels(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character_ID = ?"
    print("Running query: " + query)
    cursor.execute(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def lookup_character_count_classes(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Count(*) Total from Link_Character_Class where Character_ID = ?"
    print("Running query: " + query)
    cursor.execute(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def lookup_character_class_by_order(character_id: str, order: int):
    cursor = Connections.sql_db_connection()
    query = "Select * from Link_Character_Class Where Character_ID = ? and Number = ?"
    print("Running query: " + query)
    cursor.execute(query, [character_id, order])
    class_lookup = cursor.fetchone()
    return class_lookup.Class, class_lookup.Level


def lookup_character_feats(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select * From Link_Character_Feats Where Character_ID = ?"
    print("Running query: " + query)
    cursor.execute(query, character_id)
    rows = cursor.fetchall()
    feats = []
    for row in rows:
        feats.append(row.Feat)
    return feats


def lookup_character_gold(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select * From Main_Characters Where ID = ?"
    print("Running query: " + query)
    cursor.execute(query, [character_id])
    character = cursor.fetchone()
    return character.Gold


def lookup_character_inventory(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select * From Link_Character_Items Where Character_ID = ? Order by Item"
    print("Running query: " + query)
    cursor.execute(query, character_id)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def lookup_character_skills(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select * From Link_Character_Skills Where Character_ID = ?"
    print("Running query: " + query)
    cursor.execute(query, character_id)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        if row.Proficiency == 1:
            skills.append(row.Skill)
        else:
            skills.append(row.Skill + " (D)")
    return skills


def lookup_character_xp(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = ?"
    print("Running query: " + query)
    cursor.execute(query, character_id)
    character = cursor.fetchone()
    return character.XP


def check_level_up(character_id: str):
    character_level = lookup_character_sum_class_levels(character_id)
    character_xp = lookup_character_xp(character_id)
    cursor = Connections.sql_db_connection()
    query = "select * from Info_XP where Level = ?"
    print("Running query: " + query)
    cursor.execute(query, character_level)
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return "Yes"
    return "No"


def character_name_by_character_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = ?"
    print("Running query: " + query)
    cursor.execute(query, character_id)
    result = cursor.fetchone()
    return result.Character_Name


def character_id_by_character_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = ?"
    print("Running query: " + query)
    cursor.execute(query, character_name)
    result = cursor.fetchone()
    return result.ID
