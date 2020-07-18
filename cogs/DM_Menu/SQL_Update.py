import Connections
from DM_Menu import SQL_Lookup
from Quick_Python import run_query


def character_gold(character_id: str, gold: float):
    new_gold = float(SQL_Lookup.character_gold(character_id)) + gold

    query = "UPDATE Main_Characters " \
            "SET Gold = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [new_gold, character_id])
    cursor.commit()
    return new_gold


def character_xp(character_id: str, xp: int):
    new_xp = SQL_Lookup.character_xp(character_id) + int(xp)

    query = "UPDATE Main_Characters " \
            "SET XP = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [new_xp, character_id])
    cursor.commit()
    return new_xp


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    item_detail = SQL_Lookup.item_detail_by_character(character_id, item_name)
    new_amount = item_detail.Quantity + quantity
    query = "UPDATE Link_Character_Items set Quantity = ? " \
            "WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [new_amount, character_id, item_name])
    cursor.commit()
