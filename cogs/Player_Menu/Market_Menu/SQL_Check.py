import Connections


def character_has_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_enough_gold_to_buy_trade(gold: float):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Price <='{}'".format(gold)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True
