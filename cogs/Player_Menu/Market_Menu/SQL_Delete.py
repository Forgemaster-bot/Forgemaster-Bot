import Connections


def character_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character_ID ='{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    cursor.commit()


def trade_sale(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Main_Trade WHERE Character_ID ='{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    cursor.commit()
