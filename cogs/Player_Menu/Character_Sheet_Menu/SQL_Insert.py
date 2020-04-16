import Connections


def character_class(character_name: str, class_name: str, level: int, number: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Class (Character,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_name, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_profession(character_name: str, profession_name: str, proficiency: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Skills (Character,Skill,Proficiency) " \
                        "values ('{}','{}','{}')".format(character_name, profession_name, proficiency)
    cursor.execute(link_class_insert)
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values ('{}','{}','True')".format(book_id, spell)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_spell(character_name: str, origin: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Spells (Character_name, Origin, Spell) " \
                        "values ('{}','{}','{}')".format(character_name, origin, spell_name)
    cursor.execute(link_class_insert)
    cursor.commit()
