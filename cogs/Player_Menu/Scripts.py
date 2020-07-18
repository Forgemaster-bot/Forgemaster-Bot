from Player_Menu import SQL_Check
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Update
from Player_Menu import SQL_Insert
import random


def main_menu():
    menu_list = ['View your character sheet',
                 'Go to the workshop',
                 'Go to the market']
    return menu_list


'''''''''''''''''''''''''''''''''''''''''
############Roll Character###############
'''''''''''''''''''''''''''''''''''''''''


def rand_char(discord_id: str):
    stat_array = []
    stat_display_list = []
    for rolls in range(0, 6):  # Roll 6 times
        dice_results = []
        for roll_number in range(0, 4):  # Roll 4 dice
            dice = int(random.randint(1, 6))
            dice_results.append(dice)  # [6,3,2,6]
        lowest = False
        stat_display = []
        for roll in dice_results:
            if roll == min(dice_results) and lowest is False:  # find the first lowest roll
                formatting = '~~'
                lowest = True
            else:
                formatting = ''
            stat = '{}{}{}'.format(formatting, roll, formatting)
            if len(stat_display) == 0:
                stat_display.append('(' + stat)
            elif len(stat_display) == 3:
                stat_display.append(stat + ')')
            else:
                stat_display.append(stat)
        total_stat = sum(dice_results) - min(dice_results)
        stat_display.append(' = **{}**'.format(total_stat))
        result = stitch_list_into_string(stat_display).replace("),", ")")

        # save stats
        stat_array.append(total_stat)
        stat_display_list.append(result)
    # save to SQL after
    SQL_Insert.discord_roll(discord_id, stat_array)  # create new entry in discord roll
    # print to discord
    roll_total = sum(stat_array)
    stat_display_list.insert(0, "**{}:**".format(SQL_Lookup.player_name_by_id(discord_id)))
    stat_display_list.append('Total = **{}**'.format(roll_total))
    response = stitch_list_into_table(stat_display_list)
    return response


'''''''''''''''''''''''''''''''''''''''''
################Utility##################
'''''''''''''''''''''''''''''''''''''''''


def question_list(give_list: list):
    return_string = ""
    for entry in range(len(give_list)):
        if return_string == "":
            return_string = "{} : {}".format(entry + 1, give_list[entry])
        else:
            return_string = "{}\n{} : {}".format(return_string, entry + 1, give_list[entry])
    return return_string


def stitch_list_into_string(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}, {}".format(return_string, element)
    return return_string


def stitch_list_into_table(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}\n{}".format(return_string, element)
    return return_string


def sync_player(discord_id: str, discord_name: str):
    try:
        print("discord_id: " + discord_id + "; discord_name: " + discord_name)
        if not SQL_Check.player_exists(discord_id):
            SQL_Insert.sync_players(discord_id, discord_name)
            return True, "New"
        elif discord_name != SQL_Lookup.player_name_by_id(discord_id):
            SQL_Update.player_name(discord_name, discord_id)
            return True, "Update"
    except Exception as e:
        print(e)
        return False, "Something went wrong adding {} to the list".format(discord_name)
    return False, "No change"
