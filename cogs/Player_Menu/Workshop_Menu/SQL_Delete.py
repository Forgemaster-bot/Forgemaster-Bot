import Connections


def character_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character_ID ='{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    cursor.commit()


def wizard_spell_share(character_id: str, owner: str, spell_name):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Main_Wizard_Spell_Share " \
            "WHERE Target_ID ='{}' AND Spell = '{}' AND Owner = '{}'".format(character_id, spell_name, owner)
    cursor.execute(query)
    cursor.commit()
