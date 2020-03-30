from Mod_Menu import SQL_Lookup
from Mod_Menu import SQL_Check
from Mod_Menu import SQL_Insert
from Mod_Menu import SQL_Delete
from Mod_Menu import SQL_Update
import Update_Google_Roster
import Connections
import Quick_Python


def create_character_check(command: str):
    c_list = command.split(",")
    if len(c_list) < 12:
        return False, "You have not entered enough stats to make a character."
    if len(c_list) > 12:
        return False, "You have entered too many stats to make a character."
    discord_name = c_list[0].lstrip()
    discord_id = SQL_Lookup.player_id_by_name(c_list[0].lstrip())
    character = c_list[1].lstrip().split(" ")
    character_name = character[0].lstrip()
    if discord_id == "":
        return False, "Player name not found, please use $SyncPlayers to refresh player list and try again."
    if SQL_Check.character_exists(character_name):
        return False, "That character name is already taken, please choose another."
    # checks to see if the class is spelt correctly
    if not SQL_Check.race_exists(c_list[2].lstrip()):
        return False, "The race {} doesnt exist.".format(c_list[2].lstrip())
    if not SQL_Check.class_exists(c_list[4].lstrip()):
        return False, "The class {} doesnt exist.".format(c_list[4].lstrip())
    response = True, "Player's Discord name : {} \nName : {} \nRace : {} \nbackground : {} \n" \
                     "Class : {} \nStrength : {} \nDexterity : {} \nConstitution : {} \n" \
                     "Intelligence : {} \nWisdom : {} \nCharisma : {} \nGold : {} \n" \
                     "Do you want to make this character? [Yes/No]"\
                     .format(discord_name, character_name, c_list[2].lstrip(),
                             c_list[3].lstrip(), c_list[4].lstrip(), c_list[5].lstrip(),
                             c_list[6].lstrip(), c_list[7].lstrip(), c_list[8].lstrip(),
                             c_list[9].lstrip(), c_list[10].lstrip(), c_list[11].lstrip())
    return response


def create_character_execute(command: str):
    character_sheet = command.split(",")

    discord_id = SQL_Lookup.player_id_by_name(character_sheet[0].lstrip())
    character_sheet[0] = discord_id
    character = character_sheet[1].lstrip().split(" ")
    character_name = character[0].lstrip()
    character_sheet[1] = character_name
    character_class = character_sheet[4].lstrip()

    # update Link_character_Class
    SQL_Insert.character_create(character_sheet)
    SQL_Insert.character_class(character_name, character_class, 1, 1)
    SQL_Insert.character_item(character_name, "Rations", 10)
    Update_Google_Roster.insert_new_character(character_name)
    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_items(character_name)
    user_ping = "<@{}>".format(SQL_Lookup.character_owner(character_name))
    return "{} your character {} has been created".format(user_ping, character_name)


def character_sync_check(character_name: str):
    roster = Connections.google_sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    if character_row == 0:
        return False, "The character {} doesnt exist.".format(character_name)
    return True, "Do you want to update the SQL database with the roster information for {}?".format(character_name)


def character_sync_execute(character_name: str):
    roster = Connections.google_sheet("Roster")
    character_row = roster.col_values(2).index(character_name) + 1
    character_sheet = roster.row_values(character_row)

    # clear tables
    SQL_Update.character_sheet(character_sheet)
    SQL_Delete.clear_character_links(character_name)

    # Classes
    for col in range(4, 7):
        if character_sheet[col] == "":
            continue
        class_details = character_sheet[col].split(" ")
        character_class = class_details[0]
        character_class_level = class_details[1]
        SQL_Insert.character_class(character_name, character_class, character_class_level, col-3)

    # feats
    if len(character_sheet) < 18:
        return "{} data has been synced".format(character_name)
    if character_sheet[17] != "":
        feat_list = character_sheet[17].split(",")
        for feat in feat_list:
            SQL_Insert.character_feat(character_name, feat.lstrip())

    # Skills
    if len(character_sheet) < 20:
        return "{} data has been synced".format(character_name)

    # inventory
    if len(character_sheet) < 20:
        return "{} data has been synced".format(character_name)
    if character_sheet[19] != "":
        inventory_list = character_sheet[19].split(",")
        for item in inventory_list:
            item_details = item.replace(")", "").split(" (")
            if len(item_details) == 1:
                SQL_Insert.character_item(character_name, item_details[0].lstrip(), 1)
            else:
                SQL_Insert.character_item(character_name, item_details[0].lstrip(), item_details[1])


def character_refresh_check(character_name: str):
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, ""


def character_update_owner_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a new owner's discord ID."
    character_name = c_list[0].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    discord_id = c_list[1].lstrip()
    if not SQL_Check.player_exists(discord_id):
        return False, "Player not found, please use the command $PlayerSync"
    player_name = SQL_Lookup.player_name_by_id(discord_id)
    return True, "Change the owner of {} to {}?".format(character_name, player_name)


def add_feat_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a feat."
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    # if not SQL_Check.feat_exists(feat):
        # return False, "The feat {} doesnt exist.".format(feat)
    return True, "Give {} the feat {}?".format(character_name, feat)


def remove_feat_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a feat."
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.character_has_feat(character_name, feat):
        return False, "The character {} doesnt have the feat {}.".format(character_name, feat)
    return True, "Remove the feat {} from {}?".format(feat, character_name)


def roll_check_check(command: str):
    c_list = command.split(",")
    discord_id = SQL_Lookup.player_id_by_name(c_list[0].lstrip())
    if discord_id == "":
        return False, "Player name not found, please use $SyncPlayers to refresh player list and try again."
    return True, ""


def skill_add_check(command: str):
    c_list = command.split(",")
    if len(c_list) < 2:
        return False, "Please enter a character name and a skill."
    character_name = c_list[0].lstrip()
    skill = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.skill_exists(skill):
        return False, "The skill {} doesnt exist.".format(skill)
    if len(c_list) > 2:
        if c_list[2] != "Double":
            return False, "Only type the word double to show double proficiency"
    if SQL_Check.character_has_skill(character_name, skill):
        return False, "{} already has {}".format(character_name, skill)
    return True, "Give {} the skill {}?".format(character_name, skill)


def skill_remove_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a skill."
    character_name = c_list[0].lstrip()
    skill = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.character_has_skill(character_name, skill):
        return False, "The character {} doesnt have the skill {}".format(character_name, skill)
    return True, "Remove the skill {} from {}?".format(skill, character_name)


def stat_raise_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 3:
        return False, "Please enter a character name, the stat to raise, and the value."
    character_name = c_list[0].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    ability = c_list[1].lstrip()
    if not Quick_Python.ability_name_check(ability):
        return False, "Please enter an ability score to change [STR,DEX,CON,INT,WIS,CHA]."
    try:
        change = int(c_list[2])
    except ValueError:
        return False, "Make sure the first value is the amount of XP to give to out."
    if not SQL_Check.character_stat_max(character_name, ability, change):
        return False, "{} cant have over 20 in {}, can't add {}.".format(character_name, ability, change)
    return True, "Add {} points of {} to {}?".format(change, ability, character_name)


def character_refresh_execute(character_name: str):
    Update_Google_Roster.update_character(character_name)
    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_feat(character_name)
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_skill(character_name)


def add_feat_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()

    # get google sheet data
    SQL_Insert.character_feat(character_name, feat)
    Update_Google_Roster.update_feat(character_name)

    return "The character {} now has the feat {}".format(character_name, feat)


def remove_feat_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()

    SQL_Delete.character_feat(character_name, feat)
    Update_Google_Roster.update_feat(character_name)

    return "the feat {} has been removed from {}".format(feat, character_name)


def skill_add_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    skill = c_list[1].lstrip()
    proficiency = 1
    if len(c_list) > 2:
        proficiency = 2

    SQL_Insert.character_skill(character_name, skill, proficiency)
    Update_Google_Roster.update_skill(character_name)
    return "{} now has the skill {}".format(character_name, skill)


def skill_remove_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    skill = c_list[1].lstrip()

    SQL_Delete.character_skill(character_name, skill)
    Update_Google_Roster.update_skill(character_name)

    return "the skill {} has been removed from {}".format(skill, character_name)


def stat_change_execute(command: str):
    command_split = command.split(",")
    character_name = command_split[0].lstrip()
    ability = command_split[1].lstrip()
    value = int(command_split[2].lstrip())
    new_value = SQL_Update.character_stat_change(character_name, ability, value)
    Update_Google_Roster.update_character_ability(character_name, ability)
    return "{} now has {} in {}".format(character_name, new_value, ability)


def roll_check_execute(command: str):
    command_split = command.split(",")
    discord_name = command_split[0]
    discord_id = SQL_Lookup.player_id_by_name(discord_name)
    response = SQL_Lookup.player_stat_roll(discord_id)
    if response == "":
        return "Player hasnt rolled stats"
    else:
        return Quick_Python.stitch_string(response).replace("{},".format(discord_id), "{}:".format(discord_name))


def npc_talk_execute(command: str):
    command_split = command.split(":")
    npc = command_split[0].lstrip()
    speach = command_split[1].lstrip()
    response = "```" \
               "NPC:{}\n" \
               "{}" \
               "```".format(npc, speach)
    return response
