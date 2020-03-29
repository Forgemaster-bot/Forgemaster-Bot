import Quick_SQL


def discord_roll(discord_id):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Discord_Roll " \
            "WHERE Discord_ID ='{}'".format(discord_id)
    cursor.execute(query)
    cursor.commit()


def character(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Main_Characters WHERE Character_Name ='{}'".format(character_name)
    cursor.execute(query)
    cursor.commit()


def character_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    cursor.commit()
