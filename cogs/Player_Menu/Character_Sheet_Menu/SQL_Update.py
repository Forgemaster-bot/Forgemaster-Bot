import Connections
from Player_Menu.Character_Sheet_Menu import SQL_Lookup


def character_class_level(character_name: str, character_class: str):
    cursor = Connections.sql_db_connection()
    current_level = int(SQL_Lookup.character_class_level_by_class(character_name, character_class))
    new_level = current_level + 1
    query = "UPDATE Link_Character_Class " \
            "SET Level = '{}' " \
            "WHERE Character = '{}' AND Class = '{}'".format(new_level, character_name, character_class)
    cursor.execute(query)
    cursor.commit()


def character_subclass(character_name: str, character_class: str, subclass: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Sub_Class = '{}' " \
            "WHERE Character = '{}' AND Class = '{}'".format(subclass, character_name, character_class)
    cursor.execute(query)
    cursor.commit()
