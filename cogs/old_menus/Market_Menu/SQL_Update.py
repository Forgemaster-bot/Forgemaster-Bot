from old_menus.Market_Menu import SQL_Lookup
import Connections
from Quick_Python import run_query


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    item_detail = SQL_Lookup.character_item(character_id, item_name)
    new_amount = item_detail.Quantity + quantity
    query = "UPDATE Link_Character_Items set Quantity = ? " \
            "WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [new_amount, character_id, item_name])
    cursor.commit()


def character_gold(character_id: str, gold: float):
    new_gold = round(float(SQL_Lookup.character_gold(character_id)) + gold, 2)
    query = "UPDATE Main_Characters " \
            "SET Gold = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [new_gold, character_id])
    cursor.commit()


def trade_quantity(character_id: str, trade_good, quantity: int):
    # calculate new total
    new_amount = trade_good.Quantity + quantity
    query = "UPDATE Main_Trade set Quantity = ? " \
            "WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [new_amount, character_id, trade_good.Item])
    cursor.commit()
