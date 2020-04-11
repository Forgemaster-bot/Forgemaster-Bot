from Player_Menu.Market_Menu import SQL_Lookup
import Connections


def character_item_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    item_detail = SQL_Lookup.character_item(character_name, item_name)
    new_amount = item_detail.Quantity + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()


def character_gold(character_name: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = float(SQL_Lookup.character_gold(character_name)) + gold

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE Character_Name = '{}'".format(new_gold, character_name)
    cursor.execute(query)
    cursor.commit()


def trade_quantity(character_name: str, trade_good, quantity: int):
    # calculate new total
    new_amount = trade_good.Quantity + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Main_Trade set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, trade_good.Item)
    cursor.execute(query)
    cursor.commit()
