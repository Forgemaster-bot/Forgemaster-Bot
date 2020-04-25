from Player_Menu.Workshop_Menu import SQL_Lookup
import Connections


def character_gold(character_id: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = round(float(SQL_Lookup.character_gold(character_id)) + gold, 2)

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE ID = '{}'".format(new_gold, character_id)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_id, item_name) + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(new_amount, character_id, item_name)
    cursor.execute(query)
    cursor.commit()


def character_crafting(character_id: str, crafting_value: float, labour: int):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Main_Crafting " \
            "set Crafting_Value = '{}', Labour_Points = '{}'" \
            "WHERE Character_ID = '{}'".format(crafting_value, labour, character_id)
    cursor.execute(query)
    cursor.commit()
