from Mod_Menu import SQL_Lookup
from Mod_Menu import SQL_Check
from Mod_Menu import SQL_Insert
from Mod_Menu import SQL_Delete
from Mod_Menu import SQL_Update
import Update_Google_Roster
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
    if SQL_Check.character_exists_by_name(character_name):
        return False, "That character name is already taken, please choose another."
    # checks to see if the class is spelt correctly
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
    roll_id = SQL_Lookup.unused_roll(discord_id)

    # update Link_character_Class
    SQL_Insert.character_create(character_sheet, roll_id)
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    SQL_Insert.character_class(character_id, character_class, 1, 1)
    if character_class == 'Wizard':
        SQL_Update.character_wizard_spell(character_id, character_class)
        SQL_Insert.character_spell_book(character_id, character_name)
    SQL_Insert.character_item(character_id, "Rations", 10)
    Update_Google_Roster.insert_new_character(character_id)
    Update_Google_Roster.update_classes(character_id)
    Update_Google_Roster.update_items(character_id)
    user_ping = "<@{}>".format(SQL_Lookup.character_owner(character_id))
    return "{} your character {} has been created".format(user_ping, character_name)


def sync_players_execute(command):
    new_players = 0
    update_player = 0
    for member in command.guild.members:
        discord_name = member.display_name.replace("'", "")
        discord_id = member.id
        result = Quick_Python.sync_player(discord_id, discord_name)
        if result[0]:
            if result[1] == "New":
                new_players += 1
            elif result[1] == "Update":
                update_player += 1
        else:
            if result[1] != "No change":
                return result[1]
    return "{} new players found\n{} player names updated".format(new_players, update_player)


def add_feat_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a feat."
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    feat = c_list[1].lstrip()

    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    # if not SQL_Check.feat_exists(feat):
        # return False, "The feat {} doesnt exist.".format(feat)
    return True, "Give {} the feat {}?".format(character_name, feat)


def add_feat_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    feat = c_list[1].lstrip()

    # get google sheet data
    SQL_Insert.character_feat(character_id, feat)
    Update_Google_Roster.update_feat(character_id)

    return "The character {} now has the feat {}".format(character_name, feat)


def remove_feat_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a feat."
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    feat = c_list[1].lstrip()
    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.character_has_feat(character_name, feat):
        return False, "The character {} doesnt have the feat {}.".format(character_name, feat)
    return True, "Remove the feat {} from {}?".format(feat, character_name)


def remove_feat_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    feat = c_list[1].lstrip()

    SQL_Delete.character_feat(character_id, feat)
    Update_Google_Roster.update_feat(character_id)

    return "the feat {} has been removed from {}".format(feat, character_name)


def item_split(command: str):
    c_list = command.split(",")
    item_list = []
    if len(c_list) < 2:
        return False, "Please enter a character name and an item."
    # split input into names and items
    if SQL_Check.character_exists_by_name(c_list[0].lstrip()):
        character_name = c_list[0].lstrip()
        for rows in range(len(c_list)):
            if rows == 0:
                continue
            item_detail = c_list[rows].split(":")
            if len(item_detail) > 1:
                item_list.append([character_name, item_detail[0], item_detail[1]])
            else:
                item_list.append([character_name, item_detail[0], 1])
    else:
        item_name = c_list[0].lstrip()
        for rows in range(len(c_list)):
            if rows == 0:
                continue
            character_detail = c_list[rows].split(":")
            if len(character_detail) > 1:
                item_list.append([character_detail[0], item_name, character_detail[1]])
            else:
                item_list.append([character_detail[0], item_name, 1])
    return item_list


def item_check(command: str):  # [Character Name],[Item],[Quantity]
    item_list = item_split(command)
    return_list = []
    for rows in range(len(item_list)):
        character_name = item_list[rows][0].lstrip()
        character_id = SQL_Lookup.character_id_by_character_name(character_name)
        item_name = item_list[rows][1].lstrip()

        if character_id is False:
            return_list.append("The character {} doesnt exist.".format(character_name))
            continue
        try:
            quantity = int(item_list[rows][2])
            if quantity > 0:
                return_list.append('Add {} {} to {}'.format(quantity, item_name, character_name))
                continue
            elif quantity < 0:
                character_id = SQL_Lookup.character_id_by_character_name(character_name)
                if SQL_Check.character_has_item(character_id, item_name):
                    current_quantity = SQL_Lookup.character_item_quantity(character_id, item_name)
                    if current_quantity >= quantity*-1:
                        return_list.append('Remove {} {} from {}'.format(quantity * -1, item_name, character_name))
                    else:
                        return_list.append('{} only owns {} {} remove {}?'.format(character_name, current_quantity,
                                                                                  item_name, current_quantity))
                else:
                    return_list.append('{} doesnt own any {}, none will be removed'.format(character_name, item_name))
        except IndexError:
            return_list.append('Add {} 1 to {}'.format(character_name, item_name))
        except ValueError:
            return_list.append("{} quantity for {} was wrong and wont get any".format(character_name, item_name))
    return_list.append("Do you want to make these changes to items?")
    return Quick_Python.list_to_table(return_list)


def item_execute(command: str, author: str):
    item_list = item_split(command)
    character_name_list = []
    response_list = []
    for rows in range(len(item_list)):
        character_name = item_list[rows][0].lstrip()
        character_id = SQL_Lookup.character_id_by_character_name(character_name)
        item_name = item_list[rows][1].lstrip().replace("'", "''")

        if not SQL_Check.character_exists_by_id(character_id):
            continue
        try:
            quantity = int(item_list[rows][2])
        except IndexError:
            quantity = 1
        except ValueError:
            continue
        if quantity > 0:
            if SQL_Check.character_has_item(character_id, item_name):
                SQL_Update.character_item_quantity(character_id, item_name, quantity)
            else:
                SQL_Insert.character_item(character_id, item_name, quantity)
            response_list.append("{} received {} {}".format(character_name, quantity, item_name.replace("''", "'")))
            character_name_list.append(character_name)
        elif quantity < 0:
            if SQL_Check.character_has_item(character_id, item_name):
                current_quantity = SQL_Lookup.character_item_quantity(character_id, item_name)
                if quantity * -1 < current_quantity:
                    SQL_Update.character_item_quantity(character_id, item_name, quantity)
                else:
                    SQL_Delete.character_item(character_id, item_name)
                response_list.append("{} had {} {} removed".format(character_name, quantity,
                                                                   item_name.replace("''", "'")))
                character_name_list.append(character_name)

    for character_name in character_name_list:
        character_id = SQL_Lookup.character_id_by_character_name(character_name)
        Update_Google_Roster.update_items(character_id)
    response_list.insert(0, "{} did the following item changes:".format(author))
    return response_list


def roll_check_check(command: str):
    c_list = command.split(",")
    discord_id = SQL_Lookup.player_id_by_name(c_list[0].lstrip())
    if discord_id == "":
        return False, "Player name not found, please use $SyncPlayers to refresh player list and try again."
    return True, ""


def roll_check_execute(command: str):
    command_split = command.split(",")
    discord_name = command_split[0]
    discord_id = SQL_Lookup.player_id_by_name(discord_name)
    response = SQL_Lookup.player_stat_roll(discord_id)
    if response == "":
        return "Player hasnt rolled stats"
    else:
        return Quick_Python.list_to_string(response).replace("{},".format(discord_id), "{}:".format(discord_name))


def skill_add_check(command: str):
    c_list = command.split(",")
    if len(c_list) < 2:
        return False, "Please enter a character name and a skill."
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    skill = c_list[1].lstrip()
    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.skill_exists(skill):
        return False, "The skill {} doesnt exist.".format(skill)
    if len(c_list) > 2:
        if c_list[2] != "Double":
            return False, "Only type the word double to show double proficiency"
    if SQL_Check.character_has_skill(character_id, skill):
        return False, "{} already has {}".format(character_name, skill)
    return True, "Give {} the skill {}?".format(character_name, skill)


def skill_add_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    skill = c_list[1].lstrip()
    proficiency = 1
    if len(c_list) > 2:
        proficiency = 2

    SQL_Insert.character_skill(character_id, skill, proficiency)
    Update_Google_Roster.update_skill(character_id)
    return "{} now has the skill {}".format(character_name, skill)


def skill_remove_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a skill."
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    skill = c_list[1].lstrip()
    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.character_has_skill(character_id, skill):
        return False, "The character {} doesnt have the skill {}".format(character_name, skill)
    return True, "Remove the skill {} from {}?".format(skill, character_name)


def skill_remove_execute(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    skill = c_list[1].lstrip()

    SQL_Delete.character_skill(character_id, skill)
    Update_Google_Roster.update_skill(character_id)

    return "the skill {} has been removed from {}".format(skill, character_name)


def stat_raise_check(command: str):
    c_list = command.split(",")
    if len(c_list) != 3:
        return False, "Please enter a character name, the stat to raise, and the value."
    character_name = c_list[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    ability = c_list[1].lstrip()
    if not Quick_Python.ability_name_check(ability):
        return False, "Please enter an ability score to change [STR,DEX,CON,INT,WIS,CHA]."
    try:
        change = int(c_list[2])
    except ValueError:
        return False, "Make sure the first value is the amount of XP to give to out."
    if not SQL_Check.character_stat_max(character_id, ability, change):
        return False, "{} cant have over 20 in {}, can't add {}.".format(character_name, ability, change)
    return True, "Add {} points of {} to {}?".format(change, ability, character_name)


def stat_change_execute(command: str):
    command_split = command.split(",")
    character_name = command_split[0].lstrip()
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    ability = command_split[1].lstrip()
    value = int(command_split[2].lstrip())
    new_value = SQL_Update.character_stat_change(character_id, ability, value)
    Update_Google_Roster.update_character_ability(character_id, ability)
    return "{} now has {} in {}".format(character_name, new_value, ability)


def character_refresh_check(character_name: str):
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    if character_id is False:
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.character_exists_by_id(character_id):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, ""


def character_refresh_execute(character_name: str):
    character_id = SQL_Lookup.character_id_by_character_name(character_name)
    Update_Google_Roster.update_character(character_id)
    Update_Google_Roster.update_classes(character_id)
    Update_Google_Roster.update_feat(character_id)
    Update_Google_Roster.update_items(character_id)
    Update_Google_Roster.update_skill(character_id)


def npc_talk_execute(command: str):
    command_split = command.split(":")
    npc = command_split[0].lstrip()
    speach = command_split[1].lstrip()
    response = "```" \
               "NPC:{}\n" \
               "{}" \
               "```".format(npc, speach)
    return response
