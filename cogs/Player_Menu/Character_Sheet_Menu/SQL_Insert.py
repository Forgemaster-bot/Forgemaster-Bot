import Connections
from Quick_Python import run_query


def character_class(character_id: str, class_name: str, level: int, number: int):
    query = "insert into Link_Character_Class (Character_ID,Class,Level,Number) " \
                        "values (?,?,?,?)"
    cursor = run_query(query, [character_id, class_name, level, number])
    cursor.commit()


def character_profession(character_id: str, profession_name: str, proficiency: int):
    query = "insert into Link_Character_Skills (Character_ID,Skill,Proficiency) " \
                        "values (?,?,?)"
    cursor = run_query(query, [character_id, profession_name, proficiency])
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    query = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values (?,?,'True')"
    cursor = run_query(query, [book_id, spell])
    cursor.commit()


def character_spell(character_id: str, origin: str, spell_name: str):
    query = "insert into Link_Character_Spells (Character_ID, Origin, Spell) " \
                        "values (?,?,?)"
    cursor = run_query(query, [character_id, origin, spell_name])
    cursor.commit()


def character_spell_book(character_id: str, character_name: str, book_type: str):
    character_book = "{} Spell book".format(character_name)
    query = "insert into Main_Spell_Book (ID, Owner_ID, Name,Type) values (NEWID(),?,?,?)"
    cursor = run_query(query, [character_id, character_book, book_type])
    cursor.commit()
