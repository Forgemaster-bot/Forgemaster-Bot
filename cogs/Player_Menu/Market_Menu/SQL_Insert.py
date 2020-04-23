import Connections


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def trade_sell(character_name: str, item_name: str, quantity: int, price: float, type: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Main_Trade (Character,item,Quantity,Price, Type) " \
            "values ('{}','{}','{}','{}','{}')".format(character_name, item_name, quantity, price, type)
    cursor.execute(query)
    cursor.commit()


def share_spell(character_name: str, target_name: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Main_Wizard_Spell_Share (Target,Spell,Owner) " \
            "values ('{}','{}','{}')".format(target_name, spell_name, character_name)
    cursor.execute(query)
    cursor.commit()
