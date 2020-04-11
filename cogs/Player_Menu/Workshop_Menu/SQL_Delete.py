import Connections


def character_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name,item_name)
    cursor.execute(query)
    cursor.commit()
