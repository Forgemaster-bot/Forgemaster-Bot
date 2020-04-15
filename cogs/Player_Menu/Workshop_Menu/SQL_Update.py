from Player_Menu.Workshop_Menu import SQL_Lookup
import Connections


def character_gold(character_name: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = round(float(SQL_Lookup.character_gold(character_name)) + gold, 2)

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE Character_Name = '{}'".format(new_gold, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_item_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_name, item_name) + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()


def character_crafting(character_name: str, crafting_value: float, labour: int):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Main_Crafting " \
            "set Crafting_Value = '{}', Labour_Points = '{}'" \
            "WHERE Character_Name = '{}'".format(crafting_value, labour, character_name)
    cursor.execute(query)
    cursor.commit()
