import Connections
from Quick_Python import run_query


def discord_roll(discord_id: str, stat_array: list):
    query = "insert into Discord_Roll (ID, Discord_ID,Roll_1,Roll_2,Roll_3,Roll_4,Roll_5,Roll_6) " \
            "values (NEWID(),?,?,?,?,?,?,?)"

    cursor = run_query(query, [discord_id, stat_array[0], stat_array[1], stat_array[2], stat_array[3], stat_array[4],
                               stat_array[5]])
    cursor.commit()


def sync_players(user_id: str, name: str):
    query = "insert into Info_Discord (ID,Name,Character_Number) values (?,?,1)"
    cursor = run_query(query, [user_id, name])
    cursor.commit()
