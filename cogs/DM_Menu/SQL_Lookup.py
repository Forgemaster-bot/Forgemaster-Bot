import Quick_SQL


def character_owner(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Discord_ID


def character_gold(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_item_quantity(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def character_xp(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def character_sum_class_levels(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def log_xp(level: int):
    cursor = Quick_SQL.db_connection()
    query = "select * from Info_XP Where Level = {}".format(level)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.XP_To_Level/20
