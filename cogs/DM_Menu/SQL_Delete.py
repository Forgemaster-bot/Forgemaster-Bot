import Connections


def discord_roll(discord_id):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Discord_Roll " \
            "WHERE Discord_ID ='{}'".format(discord_id)
    cursor.execute(query)
    cursor.commit()


def character(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Main_Characters WHERE ID ='{}'".format(character_id)
    cursor.execute(query)
    cursor.commit()


def trade_sale(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Main_Trade WHERE Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    cursor.commit()

