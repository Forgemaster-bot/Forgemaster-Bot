import Connections
from DM_Menu import SQL_Lookup


def character_exists_by_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def level_up_check(character_id: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_id)
    character_xp = SQL_Lookup.character_xp(character_id)
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return True
    return False


def character_has_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True
