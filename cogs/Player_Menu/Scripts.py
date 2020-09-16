from collections import deque
import discord

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
    stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    stat_array = []
    stat_display_list = []
    discord_name = SQL_Lookup.player_name_by_id(discord_id)

    embed = discord.Embed(title=f"{discord_name} Rolled Stats:", colour=0xFFEF00)
    embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/fantasy-and-role-play-game-adventure-quest/" \
                            "512/Helmet.jpg-512.png")
    embed.description = "Your rolled stats for character creation are listed below.\n" \
                        "**Note**: You may still use point buy or stat array instead."

    for stat in stats:  # Roll 6 times
        dice = deque(sorted([random.randint(1, 6) for _ in range(0, 4)]))
        min_dice = dice.popleft()
        results_string = ', '.join(str(die) for die in dice)
        stat_value = sum(dice)
        embed.add_field(name=stat, value=f"(~~{min_dice}~~, {results_string}) = **{stat_value}**", inline=False)
        stat_array.append(stat_value)
    # save to SQL after
    SQL_Insert.discord_roll(discord_id, stat_array)  # create new entry in discord roll
    # print to discord
    embed.add_field(name='Total', value=f"{sum(stat_array)}", inline=False)
    return embed


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
