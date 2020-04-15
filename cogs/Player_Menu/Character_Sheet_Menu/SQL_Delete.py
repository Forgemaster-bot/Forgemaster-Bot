import Connections


def character_forget_spell(character_name: str, class_name: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    query = "Delete " \
            "From Link_Character_Spells " \
            "Where Character_name = '{}' and Origin = '{}' and Spell = '{}'"\
        .format(character_name, class_name, spell_name)
    cursor.execute(query)
    cursor.commit()
