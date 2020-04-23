import Connections


def character_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name,item_name)
    cursor.execute(query)
    cursor.commit()


def wizard_spell_share(character_name: str, owner: str, spell_name):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Main_Wizard_Spell_Share " \
            "WHERE Target ='{}' AND Spell = '{}' AND Owner = '{}'".format(character_name, spell_name, owner)
    cursor.execute(query)
    cursor.commit()
