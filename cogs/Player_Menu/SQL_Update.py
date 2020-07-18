import Connections
from Quick_Python import run_query


def player_name(discord_name: str, discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Info_Discord " \
            "SET Name = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [discord_name, discord_id])
    cursor.commit()
