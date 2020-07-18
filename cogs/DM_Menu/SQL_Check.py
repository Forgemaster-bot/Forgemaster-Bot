import Connections
from DM_Menu import SQL_Lookup
from Quick_Python import run_query


def character_exists_by_id(character_id: str):
    query = "select * " \
            "from Main_Characters " \
            "where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def level_up_check(character_id: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_id)
    character_xp = SQL_Lookup.character_xp(character_id)
    query = "select * " \
            "from Info_XP " \
            "where Level = ?"
    cursor = run_query(query, [character_level])
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return True
    return False


def character_has_item(character_id: str, item_name: str):
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return True
