from DM_Menu import SQL_Check
from DM_Menu import SQL_Lookup
from DM_Menu import SQL_Delete
from DM_Menu import SQL_Insert
from DM_Menu import SQL_Update


import Update_Google_Roster
import Quick_Python


def kill_character_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter one character and a cause of death."
    character_name = c_list[0].lstrip()
    reason = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, "did {} die by {}?".format(character_name, reason)


def kill_character_execute(command: str):
    c_list = command.split(",")
    character_name = c_list[0]
    reason = c_list[1]
    discord_id = SQL_Lookup.character_owner(character_name.lstrip())

    SQL_Delete.discord_roll(discord_id)
    SQL_Insert.move_to_graveyard(character_name.lstrip(), reason.lstrip())
    SQL_Delete.character(character_name.lstrip())

    Update_Google_Roster.kill_character(command)
    return "{} died because {}".format(character_name, reason)


def add_gold_check(command: str):  # [Gold],[Character 1],[Character 2]
    c_list = command.split(",")
    try:
        gold = float(c_list[0])
    except ValueError:
        return False, "Make sure the first value is the gold given to each characters."
    del c_list[0]
    if len(c_list) == 0:
        return False, "Please enter at least one character name."
    # loop through each character
    paid_characters = []
    for character_name in c_list:
        # check if the character exists
        if not SQL_Check.character_exists(character_name.lstrip()):
            return False, "The character {} doesnt exist.".format(character_name)
        paid_characters.append(character_name.lstrip())
    return True, "Give {} gold to {}?".format(gold, Quick_Python.list_to_string(paid_characters))


def add_gold_execute(command: str):  # [Gold],[Character 1],[Character 2]
    # get inputs data
    c_list = command.split(",")
    gold = float(c_list[0])
    del c_list[0]
    # loop through each character
    for character_name in c_list:
        # find the row the character is on
        SQL_Update.character_gold(character_name.lstrip(), gold)
    Update_Google_Roster.update_gold_group(c_list)
    return "{} Gold has been added to {}".format(gold, Quick_Python.list_to_string(c_list))


def add_xp_check(command: str):
    c_list = command.split(",")
    try:
        xp = int(c_list[0])
    except ValueError:
        return False, "Make sure the first value is the amount of XP to give to out."
    del c_list[0]
    if len(c_list) == 0:
        return False, "Please enter at least one character name."
    # loop through each character
    for character_name in c_list:
        # check if the character exists
        if not SQL_Check.character_exists(character_name.lstrip()):
            return False, "The character {} doesnt exist.".format(character_name)
    return True, "Give {} xp to {}?".format(xp, Quick_Python.list_to_string(c_list))


def add_xp_execute(command: str):  # [Gold],[Character 1],[Character 2]
    # get inputs data
    c_list = command.split(",")
    xp = int(c_list[0])
    del c_list[0]

    # loop through each character
    for character_name in c_list:
        # find the row the character is on
        SQL_Update.character_xp(character_name.lstrip(), xp)
    Update_Google_Roster.update_xp_group(c_list)
    return "{} xp has been added to {}".format(xp, Quick_Python.list_to_string(c_list))


def log_xp_check(character_name: str):
    if not SQL_Check.character_exists(character_name.lstrip()):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, ""


def log_xp_execute(character_name: str, author: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    if SQL_Check.level_up_check(character_name):
        character_level += 1
    xp = SQL_Lookup.log_xp(character_level)
    SQL_Update.character_xp(character_name.lstrip(), xp)
    c_list = [character_name]
    Update_Google_Roster.update_xp_group(c_list)
    return "{} got {}xp from {} for posting a log".format(character_name, xp, author)


def npc_talk_execute(command: str):
    command_split = command.split(":")
    npc = command_split[0].lstrip()
    speech = command_split[1].lstrip()
    response = "```" \
               "NPC:{}\n" \
               "{}" \
               "```".format(npc, speech)
    return response
