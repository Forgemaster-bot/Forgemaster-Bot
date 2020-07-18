import Connections
import textwrap
from Quick_Python import run_query


def player_character_list(discord_id: str):
    query = "select Character_Name from Main_Characters where Discord_ID = ?"
    cursor = run_query(query, [discord_id])
    response = []
    for row in cursor.fetchall():
        response.append(row.Character_Name)
    return response


def player_stat_roll(discord_id: str):
    query = textwrap.dedent("""
    select B.Character_Name, A.* 
    from Discord_Roll A 
    left join Main_Characters B on A.ID = B.Roll_ID 
    where A.Discord_ID = ?
    order by Character_Name
    """)
    cursor = run_query(query, [discord_id])
    result = cursor.fetchall()
    if result is None:
        return ""
    return result


def player_name_by_id(user_id: str):
    query = "select * from Info_Discord where ID = ?"
    cursor = run_query(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def character_id_by_character_name(character_name: str):
    query = "select * from Main_Characters where Character_Name = ?"
    cursor = run_query(query, [character_name])
    result = cursor.fetchone()
    return result.ID


def character_name_by_character_id(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Character_Name


def character_total(discord_id: str):
    query = "select count(*) as Total from Main_Characters where Discord_ID = ?"
    cursor = run_query(query, [discord_id])
    result = cursor.fetchone()
    return result.Total


def character_roll_total(discord_id: str):
    query = "select count(*) as Total from Discord_roll where Discord_ID = ?"
    cursor = run_query(query, [discord_id])
    result = cursor.fetchone()
    return result.Total


def total_characters_allowed(discord_id: str):
    query = "select * from Info_Discord where ID = ?"
    cursor = run_query(query, [discord_id])
    result = cursor.fetchone()
    return result.Character_Number
