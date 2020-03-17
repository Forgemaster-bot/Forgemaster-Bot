import Quick_SQL
from Player_Menu import SQL_Lookup


def character_gold(character_name: str, gold: float):
    cursor = Quick_SQL.db_connection()
    new_gold = float(SQL_Lookup.character_gold_total(character_name)) + gold

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE Character_Name = '{}'".format(new_gold, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_main_crafting(character_name: str, craft_points: int, crafting_value: float, labour: int):
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Main_Crafting " \
            "set Crafting_Point = '{}', Crafting_Value = '{}', Labour_Points = '{}'" \
            "WHERE Character_Name = '{}'".format(craft_points, crafting_value, labour, character_name)
    cursor.execute(query)
    cursor.commit()


def character_item_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_name, item_name) + quantity
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()


def character_class_level(character_name: str, character_class: str):
    cursor = Quick_SQL.db_connection()
    current_level = int(SQL_Lookup.character_class_level_by_class(character_name, character_class))
    new_level = current_level + 1
    query = "UPDATE Link_Character_Class " \
            "SET Level = '{}' " \
            "WHERE Character = '{}' AND Class = '{}'".format(new_level, character_name, character_class)
    cursor.execute(query)
    cursor.commit()


def trade_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    trade_good = SQL_Lookup.trade_item_details("", item_name)
    new_amount = trade_good.Quantity + quantity
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Main_Trade set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()


def crafting_points(character_name: str, craft_points: int, crafting_value: float, labour: int):
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Main_Crafting " \
            "set Crafting_Point = '{}', Crafting_Value = '{}', Labour_Points = '{}'" \
            "WHERE Character_Name = '{}'".format(craft_points, crafting_value, labour, character_name)
    cursor.execute(query)
    cursor.commit()
