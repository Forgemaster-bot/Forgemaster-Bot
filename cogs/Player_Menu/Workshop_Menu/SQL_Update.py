from Player_Menu.Workshop_Menu import SQL_Lookup
from Quick_Python import run_query


def character_gold(character_id: str, gold: float):
    new_gold = round(float(SQL_Lookup.character_gold(character_id)) + gold, 2)

    query = "UPDATE Main_Characters " \
            "SET Gold = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [new_gold, character_id])
    cursor.commit()
    return new_gold


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_id, item_name) + quantity
    query = "UPDATE Link_Character_Items set Quantity = ? " \
            "WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [new_amount, character_id, item_name])
    cursor.commit()


def character_crafting(character_id: str, crafting_value: float, labour: int):
    query = "UPDATE Main_Crafting " \
            "set Crafting_Value = ?, Labour_Points = ?" \
            "WHERE Character_ID = ?"
    cursor = run_query(query, [crafting_value, labour, character_id])
    cursor.commit()
