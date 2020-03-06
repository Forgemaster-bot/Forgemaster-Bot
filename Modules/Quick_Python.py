import random
import SQL_Check
import SQL_Lookup
import SQL_Update
import SQL_Insert

def stitch_string(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}, {}".format(return_string, element)
    return return_string


def stitch_table(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}\n{}".format(return_string, element)
    return return_string


def find_character_row(character_list: list, character_name: str):
    try:
        character_row = character_list.index(character_name) + 1
    except ValueError:
        character_row = 0
    return character_row


def find_trade(character_list: list, character_name: str, item_list: list, item_name: str):
    for character in character_list:
        if character == character_name:
            character_index = character_list.index(character_name)
            if item_list[character_index] == item_name:
                return character_index + 1
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


def sync_player(discord_id: str, discord_name: str):
    try:
        if not SQL_Check.player_exists(discord_id):
            SQL_Insert.sync_players(discord_id, discord_name)
            return True, "New"
        elif discord_name != SQL_Lookup.player_name_by_id(discord_id):
            SQL_Update.player_name(discord_name, discord_id)
            return True, "Update"
    except:
        return False, "Something went wrong adding {} to the list".format(discord_name)
    return False, "No change"


def question_list(give_list: list):
    return_string = ""
    list_length = len(give_list)
    for entry in range(list_length):
        if return_string == "":
            return_string = "{} : {}".format(entry + 1, give_list[entry])
        else:
            return_string = "{}\n{} : {}".format(return_string, entry + 1, give_list[entry])
    return return_string

