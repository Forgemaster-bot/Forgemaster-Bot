import Connections


def player_character_list(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Character_Name from Main_Characters where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    rows = cursor.execute(query)
    response = []
    for row in rows:
        response.append(row.Character_Name)
    return response


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select B.Character_Name, A.* " \
            "from Discord_Roll A " \
            "left join Main_Characters B " \
            "on A.ID = B.Roll_ID " \
            "where A.Discord_ID = '{}' " \
            "order by Character_Name".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchall()
    if result is None:
        return ""
    return result


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID = '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def character_id_by_character_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.ID


def character_name_by_character_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Character_Name


def character_total(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total from Main_Characters where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_roll_total(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total from Discord_roll where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def total_characters_allowed(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID = '{}' ".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Character_Number
