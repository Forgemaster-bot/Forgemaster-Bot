import Connections
from DM_Menu import SQL_Lookup


def character_gold(character_id: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = float(SQL_Lookup.character_gold(character_id)) + gold

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE ID = '{}'".format(new_gold, character_id)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_xp(character_id: str, xp: int):
    cursor = Connections.sql_db_connection()
    new_xp = SQL_Lookup.character_xp(character_id) + int(xp)

    query = "UPDATE Main_Characters " \
            "SET XP = {} " \
            "WHERE ID = '{}'".format(new_xp, character_id)
    cursor.execute(query)
    cursor.commit()
    return new_xp


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    item_detail = SQL_Lookup.item_detail_by_character(character_id, item_name)
    new_amount = item_detail.Quantity + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(new_amount, character_id, item_name)
    cursor.execute(query)
    cursor.commit()
