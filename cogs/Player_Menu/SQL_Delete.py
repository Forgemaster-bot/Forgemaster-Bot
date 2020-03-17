import Quick_SQL


def character_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name,item_name)
    cursor.execute(query)
    cursor.commit()


def trade_sale(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Main_Trade WHERE Character ='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    cursor.commit()