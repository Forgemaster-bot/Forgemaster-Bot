import Connections
from DM_Menu import SQL_Lookup


def character_gold(character_name: str, gold: float):
    cursor = Connections.sql_db_connection()
    new_gold = float(SQL_Lookup.character_gold(character_name)) + gold

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE Character_Name = '{}'".format(new_gold, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_xp(character_name: str, xp: int):
    cursor = Connections.sql_db_connection()
    new_xp = SQL_Lookup.character_xp(character_name) + int(xp)

    query = "UPDATE Main_Characters " \
            "SET XP = {} " \
            "WHERE Character_Name = '{}'".format(new_xp, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_xp