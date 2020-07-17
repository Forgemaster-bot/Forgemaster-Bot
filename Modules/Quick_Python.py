import random
import Connections


def list_to_string(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}, {}".format(return_string, element)
    return return_string


def list_to_table(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}\n{}".format(return_string, element)
    return return_string


def find_character_row(character_list: list, character_name: str):
    for row in range(len(character_list)):
        target = character_list[row].lower()
        if target == character_name.lower():
            return row + 1
    return 0


def ability_name_check(stat: str):
    stat_list = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    for name in stat_list:
        if name == stat:
            return True
    return False


def ability_name_convert(ability: str):
    if ability == 'STR':
        return 'Strength'
    elif ability == 'DEX':
        return 'Dexterity'
    elif ability == 'CON':
        return 'Constitution'
    elif ability == 'INT':
        return 'Intelligence'
    elif ability == 'WIS':
        return 'Wisdom'
    elif ability == 'CHA':
        return 'Charisma'


def dice_roll(low: int, high: int):
    response = random.randint(low, high)
    return response


def question_list(give_list: list):
    return_string = ""
    list_length = len(give_list)
    for entry in range(list_length):
        if return_string == "":
            return_string = "{} : {}".format(entry + 1, give_list[entry])
        else:
            return_string = "{}\n{} : {}".format(return_string, entry + 1, give_list[entry])
    return return_string


def find_trade_row(seller_name: str, seller_list: list, item_name: str, item_list: list):
    for row in range(len(seller_list)):
        if seller_list[row].lower() == seller_name.lower():
            character_index = row
            list_item_name = item_list[character_index]
            if list_item_name.lower() == item_name.lower():
                trade_row = character_index + 1
                return trade_row


def check_player_exists(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Discord where ID= '{}' ".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def sync_player(discord_id: str, discord_name: str):
    try:
        if not check_player_exists(discord_id):
            insert_players(discord_id, discord_name)
            return True, "New"
        elif discord_name != lookup_player_name_by_id(discord_id):
            update_player_name(discord_name, discord_id)
            return True, "Update"
    except Exception as e:
        print(e)
        return False, "Something went wrong adding {} to the list".format(discord_name)
    return False, "No change"


def insert_players(user_id: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "insert into Info_Discord (ID,Name,Character_Number) values ('{}','{}',1)".format(user_id, name)
    cursor.execute(query)
    cursor.commit()


def lookup_player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def update_player_name(discord_name: str, discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Info_Discord " \
            "SET Name = '{}' " \
            "WHERE ID = '{}'".format(discord_name, discord_id)
    cursor.execute(query)
    cursor.commit()
