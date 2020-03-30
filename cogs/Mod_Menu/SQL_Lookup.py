import Connections


def player_id_by_name(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.ID


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result


def character_owner(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Discord_ID


def character_ability_score(character_name: str, ability: str):
    cursor = Connections.sql_db_connection()
    sql_command = "select * from Main_Characters where Character_Name = '{}'".format(character_name)
    cursor.execute(sql_command)
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
