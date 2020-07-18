import Connections
from Quick_Python import run_query


def character_owner(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_gold(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    character = cursor.fetchone()
    return character.Gold


def character_xp(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    character = cursor.fetchone()
    return character.XP


def character_sum_class_levels(character_id: str):
    query = "select SUM(Level) Total from Link_Character_Class where Character_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def log_xp(level: int):
    query = "select * from Info_XP Where Level = ?"
    cursor = run_query(query, [level])
    result = cursor.fetchone()
    return result.XP_To_Level/20


def character_id_by_character_name(character_id: str):
    query = "select * from Main_Characters where Character_Name = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.ID


def character_trade_items(character_id: str):
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character_ID = ? " \
            "order by Item"
    cursor = run_query(query, [character_id])
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Item)
    return result


def trade_item_by_character(character_id: str, item_name: str):
    query = "select * " \
            "From Main_Trade " \
            "Where Item = ? and Character_ID = ? " \
            "order by Price, Quantity desc"
    cursor = run_query(query, [item_name, character_id])
    item = cursor.fetchone()
    return item


def item_detail_by_character(character_id: str, item_name: str):
    query = "select * from Link_Character_Items where Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    item = cursor.fetchone()
    return item
