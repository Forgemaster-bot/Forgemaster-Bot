import Connections


def character_exists(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select Character_Name " \
            "From Main_Characters " \
            "Where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_exists(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Discord where ID='{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}' ".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True
