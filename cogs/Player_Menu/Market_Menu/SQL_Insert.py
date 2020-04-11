import Connections


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def trade_sell(character_name: str, item_name: str, quantity: int, price: float):
    cursor = Connections.sql_db_connection()
    query = "insert into Main_Trade (Character,item,Quantity,Price) " \
            "values ('{}','{}','{}','{}')".format(character_name, item_name, quantity, price)
    cursor.execute(query)
    cursor.commit()
