import Connections


def character_owner(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_gold(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_xp(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def character_sum_class_levels(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character_ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def log_xp(level: int):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_XP Where Level = {}".format(level)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.XP_To_Level/20


def character_id_by_character_name(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.ID


def character_trade_items(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character_ID = '{}' " \
            "order by Item".format(character_id)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Item)
    return result


def trade_item_by_character(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character_ID = '{}' " \
            "order by Price, Quantity desc".format(item_name, character_id)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def item_detail_by_character(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character_ID = '{}' AND Item = '{}'".format(character_id,
                                                                                                  item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item
