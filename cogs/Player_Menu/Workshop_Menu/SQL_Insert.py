import Connections
from Quick_Python import run_query


def crafting(character_id: str):
    query = "insert into Main_crafting (character_ID,Crafting_Value,Labour_Points) " \
             "values (?,'50','0')"
    cursor = run_query(query, [character_id])
    cursor.commit()


def character_item(character_id: str, item_name: str, quantity: int):
    query = "insert into Link_Character_Items (Character_ID,Item,Quantity) " \
                        "values (?,?,?)"
    cursor = run_query(query, [character_id, item_name, quantity])
    cursor.commit()


def character_recipe(character_id: str, profession: str, recipe_name: str):
    query = "insert into Link_Character_Recipe (Character_ID,Skill,Recipe) " \
                        "values (?,?,?)"
    cursor = run_query(query, [character_id, profession, recipe_name])
    cursor.commit()


def spell_book_spell(book_id: int, spell: str):
    query = "insert into Link_Spell_book_Spells (Spell_Book_ID, Spell, Known) " \
                        "values (?,?,'True')"
    cursor = run_query(query, [book_id, spell])
    cursor.commit()
