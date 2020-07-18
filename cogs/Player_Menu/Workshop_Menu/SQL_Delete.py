import Connections
from Quick_Python import run_query


def character_item(character_id: str, item_name: str):
    query = "DELETE FROM Link_Character_Items WHERE Character_ID =? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    cursor.commit()


def wizard_spell_share(character_id: str, owner: str, spell_name):
    query = "DELETE FROM Main_Wizard_Spell_Share " \
            "WHERE Target_ID =? AND Spell = ? AND Owner = ?"
    cursor = run_query(query, [character_id, spell_name, owner])
    cursor.commit()
