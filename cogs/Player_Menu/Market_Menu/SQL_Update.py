from Player_Menu.Market_Menu import SQL_Lookup
import Connections


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    item_detail = SQL_Lookup.character_item(character_id, item_name)
    new_amount = item_detail.Quantity + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(new_amount, character_id, item_name)
    cursor.execute(query)
    cursor.commit()


def character_gold(character_id: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = round(float(SQL_Lookup.character_gold(character_id)) + gold, 2)

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE ID = '{}'".format(new_gold, character_id)
    cursor.execute(query)
    cursor.commit()


def trade_quantity(character_id: str, trade_good, quantity: int):
    # calculate new total
    new_amount = trade_good.Quantity + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Main_Trade set Quantity = '{}' " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(new_amount, character_id, trade_good.Item)
    cursor.execute(query)
    cursor.commit()
