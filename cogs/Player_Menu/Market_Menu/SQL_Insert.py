import Connections


def character_item(character_id: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character_ID ,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_id, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def trade_sell(character_id: str, item_name: str, quantity: int, price: float, item_type: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Main_Trade (Character_ID,item,Quantity,Price, Type) " \
            "values ('{}','{}','{}','{}','{}')".format(character_id, item_name, quantity, price, item_type)
    cursor.execute(query)
    cursor.commit()


def share_spell(owner_name: str, target_name: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Main_Wizard_Spell_Share (Target,Spell,Owner) " \
            "values ('{}','{}','{}')".format(target_name, spell_name, owner_name)
    cursor.execute(query)
    cursor.commit()
