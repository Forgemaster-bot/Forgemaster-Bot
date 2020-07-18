import Connections
from Quick_Python import run_query


def character_forget_spell(character_id: str, class_name: str, spell_name: str):
    query = "Delete " \
            "From Link_Character_Spells " \
            "Where Character_ID = ? and Origin = ? and Spell = ?"
    cursor = run_query(query, [character_id, class_name, spell_name])
    cursor.commit()
