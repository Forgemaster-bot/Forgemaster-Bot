import Connections


def discord_roll(discord_id: str, stat_array: list):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Discord_Roll (ID, Discord_ID,Roll_1,Roll_2,Roll_3,Roll_4,Roll_5,Roll_6) " \
                        "values (NEWID(),'{}','{}','{}','{}','{}','{}','{}')".format(discord_id,
                                                                                     stat_array[0], stat_array[1],
                                                                                     stat_array[2], stat_array[3],
                                                                                     stat_array[4], stat_array[5])
    cursor.execute(link_class_insert)
    cursor.commit()


def sync_players(user_id: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Info_Discord (ID,Name,Character_Number) values ('{}','{}',1)".format(user_id, name)
    cursor.execute(query)
    cursor.commit()
