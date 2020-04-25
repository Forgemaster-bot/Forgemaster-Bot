import Connections


def character_forget_spell(character_id: str, class_name: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    query = "Delete " \
            "From Link_Character_Spells " \
            "Where Character_ID = '{}' and Origin = '{}' and Spell = '{}'"\
        .format(character_id, class_name, spell_name)
    cursor.execute(query)
    cursor.commit()
