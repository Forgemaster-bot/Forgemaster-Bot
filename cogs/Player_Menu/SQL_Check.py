import Connections
from Quick_Python import run_query


def character_exists(character_id: str):
    query = "Select Character_Name " \
            "From Main_Characters " \
            "Where Character_Name = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_exists(user_id: str):
    query = "select * " \
            "from Info_Discord where ID=?"
    cursor = run_query(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_stat_roll(discord_id: str):
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = ? "
    cursor = run_query(query, [discord_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True
