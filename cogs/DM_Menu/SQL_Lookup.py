import Connections


def character_owner(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Discord_ID


def character_gold(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_xp(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def character_sum_class_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def log_xp(level: int):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_XP Where Level = {}".format(level)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.XP_To_Level/20
