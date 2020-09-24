import Connections
from Quick_Python import run_query


def character_has_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_enough_gold_to_buy_trade(gold: float):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Price <= ?"
    cursor = run_query(query, [gold])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_is_wizard(character_id: str, ):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character_ID = ? and Class = 'Wizard'"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return None
    return True
