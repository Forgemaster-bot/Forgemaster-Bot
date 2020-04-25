import Connections
from Player_Menu.Character_Sheet_Menu import SQL_Lookup


def character_class_level(character_id: str, class_name: str):
    cursor = Connections.sql_db_connection()
    current_level = int(SQL_Lookup.character_class_level_by_class(character_id, class_name))
    new_level = current_level + 1
    query = "UPDATE Link_Character_Class " \
            "SET Level = '{}' " \
            "WHERE Character_ID = '{}' AND Class = '{}'".format(new_level, character_id, class_name)
    cursor.execute(query)
    cursor.commit()


def character_subclass(character_id: str, class_name: str, subclass: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Sub_Class = '{}' " \
            "WHERE Character_ID = '{}' AND Class = '{}'".format(subclass, character_id, class_name)
    cursor.execute(query)
    cursor.commit()


def character_forget_spell_allow(character_id: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Replace_Spell = 1 " \
            "WHERE Character_ID = '{}' AND Class = '{}'".format(character_id, class_name)
    cursor.execute(query)
    cursor.commit()


def character_forget_spell_stop(character_id: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Replace_Spell = 0 " \
            "WHERE Character_ID = '{}' AND Class = '{}'".format(character_id, class_name)
    cursor.execute(query)
    cursor.commit()


def character_wizard_spell(character_id: str, class_name: str, spell_number: int):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Free_Wizard_Spells = '{}' " \
            "WHERE Character_ID = '{}' AND Class = '{}'".format(spell_number, character_id, class_name)
    cursor.execute(query)
    cursor.commit()
