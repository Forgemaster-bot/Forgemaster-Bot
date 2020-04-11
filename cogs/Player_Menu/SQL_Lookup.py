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
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


