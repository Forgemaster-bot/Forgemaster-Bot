import Connections
import textwrap


def player_id_by_name(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where Name = ?"
    cursor.execute(query, [name])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.ID


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID = ?"
    cursor.execute(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = textwrap.dedent("""
    select * 
    from Discord_Roll 
    where Discord_ID = ?
    """)
    cursor.execute(query, [discord_id])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result


def character_owner(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID=?"
    cursor.execute(query, character_id)
    result = cursor.fetchone()
    return result.Discord_ID


def character_ability_score(character_id: str, ability: str):
    cursor = Connections.sql_db_connection()
    sql_command = "select * from Main_Characters where ID = ?"
    cursor.execute(sql_command, [character_id])
    result = cursor.fetchone()
    value = 0
    if ability == "STR":
        value = result.Strength
    if ability == "DEX":
        value = result.Dexterity
    if ability == "CON":
        value = result.Constitution
    if ability == "INT":
        value = result.Intelligence
    if ability == "WIS":
        value = result.Wisdom
    if ability == "CHA":
        value = result.Charisma
    return value


def character_item_quantity(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character_ID = ? AND Item = ?"
    cursor.execute(query, [character_id, item_name])
    item = cursor.fetchone()
    return item.Quantity


def character_id_by_character_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = ?"
    cursor.execute(query, [character_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return result.ID


def character_name_by_character_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = ?".format(character_id)
    cursor.execute(query, [character_id])
    result = cursor.fetchone()
    return result.Character_Name


def unused_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = textwrap.dedent("""
    select B.Character_Name, A.* 
    from Discord_Roll A 
    left join Main_Characters B on A.ID = B.Roll_ID 
    where A.Discord_ID = ? and B.Character_Name is NULL
    """)
    cursor.execute(query, [discord_id])
    result = cursor.fetchone()
    return result.ID
