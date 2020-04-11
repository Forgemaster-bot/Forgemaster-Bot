import Connections


def player_name(discord_name: str, discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Info_Discord " \
            "SET Name = '{}' " \
            "WHERE ID = '{}'".format(discord_name, discord_id)
    cursor.execute(query)
    cursor.commit()
