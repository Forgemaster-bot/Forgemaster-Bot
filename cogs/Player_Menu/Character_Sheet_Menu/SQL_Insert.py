import Connections


def character_class(character_id: str, class_name: str, level: int, number: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Class (Character_ID,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_id, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_profession(character_id: str, profession_name: str, proficiency: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Skills (Character_ID,Skill,Proficiency) " \
                        "values ('{}','{}','{}')".format(character_id, profession_name, proficiency)
    cursor.execute(link_class_insert)
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values ('{}','{}','True')".format(book_id, spell)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_spell(character_id: str, origin: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Spells (Character_ID, Origin, Spell) " \
                        "values ('{}','{}','{}')".format(character_id, origin, spell_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_spell_book(character_id: str, character_name: str, book_type: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Main_Spell_Book (ID, Owner_ID, Name,Type) " \
                        "values (NEWID(),'{}','{} Spell book','{}')".format(character_id, character_name, book_type)
    cursor.execute(link_class_insert)
    cursor.commit()
