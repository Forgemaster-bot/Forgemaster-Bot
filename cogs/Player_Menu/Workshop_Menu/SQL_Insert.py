import Connections


def crafting(character_name: str):
    cursor = Connections.sql_db_connection()
    insert = "insert into Main_crafting (character_Name,Crafting_Value,Labour_Points) " \
             "values ('{}','50','0')".format(character_name)
    cursor.execute(insert)
    cursor.commit()


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_recipe(character_name: str, profession: str, recipie_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Recipe (Character,Skill,Recipe) " \
                        "values ('{}','{}','{}')".format(character_name, profession, recipie_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values ('{}','{}','True')".format(book_id, spell)
    cursor.execute(link_class_insert)
    cursor.commit()
