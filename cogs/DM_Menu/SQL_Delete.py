import Connections
from Quick_Python import run_query


def discord_roll(discord_id):
    query = "DELETE FROM Discord_Roll " \
            "WHERE Discord_ID = ?"
    cursor = run_query(query, [discord_id])
    cursor.commit()


def character(character_id: str):
    query = "DELETE FROM Main_Characters WHERE ID = ?"
    cursor = run_query(query, [character_id])
    cursor.commit()


def trade_sale(character_id: str, item_name: str):
    query = "DELETE FROM Main_Trade WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    cursor.commit()

