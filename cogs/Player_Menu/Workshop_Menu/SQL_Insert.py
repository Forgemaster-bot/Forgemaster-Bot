import Connections


def crafting(character_id: str):
    cursor = Connections.sql_db_connection()
    insert = "insert into Main_crafting (character_ID,Crafting_Value,Labour_Points) " \
             "values ('{}','50','0')".format(character_id)
    cursor.execute(insert)
    cursor.commit()


def character_item(character_id: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character_ID,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_id, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_recipe(character_id: str, profession: str, recipie_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Recipe (Character_ID,Skill,Recipe) " \
                        "values ('{}','{}','{}')".format(character_id, profession, recipie_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values ('{}','{}','True')".format(book_id, spell)
    cursor.execute(link_class_insert)
    cursor.commit()
