import Quick_SQL


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def crafting_point(character_name: str):
    cursor = Quick_SQL.db_connection()
    insert = "insert into Main_crafting (character_Name,Crafting_Point,Crafting_Value,Labour_Points) " \
             "values ('{}','1','100','0')".format(character_name)
    cursor.execute(insert)
    cursor.commit()


def character_class(character_name: str, class_name: str, level: int, number: int):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Class (Character,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_name, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def trade_sell(character_name: str, item_name: str, quantity: int, price: float):
    cursor = Quick_SQL.db_connection()
    query = "insert into Main_Trade (Character,item,Quantity,Price) " \
            "values ('{}','{}','{}','{}')".format(character_name, item_name, quantity, price)
    cursor.execute(query)
    cursor.commit()
