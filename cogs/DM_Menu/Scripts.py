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
    return True, "Give {} gold to {}?".format(gold, Quick_Python.stitch_string(paid_characters))


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
    return "{} Gold has been added to {}".format(gold, Quick_Python.stitch_string(c_list))


def item_check(command: str):  # [Character Name],[Item],[Quantity]
    item_list = item_split(command)
    return_list = []
    for rows in range(len(item_list)):
        character_name = item_list[rows][0].lstrip()
        item_name = item_list[rows][1].lstrip()

        if not SQL_Check.character_exists(character_name):
            return_list.append("The character {} doesnt exist.".format(character_name))
            continue
        try:
            quantity = int(item_list[rows][2])
            if quantity > 0:
                return_list.append('Add {} {} to {}'.format(quantity, item_name, character_name))
                continue
            elif quantity < 0:
                if SQL_Check.character_has_item(character_name, item_name):
                    current_quantity = SQL_Lookup.character_item_quantity(character_name, item_name)
                    if current_quantity >= quantity:
                        return_list.append('Remove {} {} from {}'.format(quantity * -1, item_name, character_name))
                    else:
                        return_list.append('{} only owns {} {}'.format(character_name, current_quantity, item_name))
                else:
                    return_list.append('{} doesnt own any {}, none will be removed'.format(character_name, item_name))
        except IndexError:
            return_list.append('Add {} 1 to {}'.format(character_name, item_name))
        except ValueError:
            return_list.append("{} quantity for {} was wrong and wont get any".format(character_name, item_name))
    return_list.append("Do you want to make these changes to items?")
    return Quick_Python.stitch_table(return_list)


def item_execute(command: str):
    item_list = item_split(command)
    character_name_list = []
    response_list = []
    for rows in range(len(item_list)):
        character_name = item_list[rows][0].lstrip()
        item_name = item_list[rows][1].lstrip()
        try:
            quantity = int(item_list[rows][2])
        except IndexError:
            quantity = 1
        except ValueError:
            continue
        if quantity > 0:
            if SQL_Check.character_has_item(character_name, item_name):
                SQL_Update.character_item_quantity(character_name, item_name, quantity)
                new_quantity = SQL_Lookup.character_item_quantity(character_name, item_name)
                response_list.append("{} now has {} {}".format(character_name_list, new_quantity, item_name))
            else:
                SQL_Insert.character_item(character_name, item_name, quantity)
                response_list.append("{} now has {} {}".format(character_name_list, quantity, item_name))
            character_name_list.append(character_name)
        elif quantity < 0:
            if SQL_Check.character_has_item(character_name, item_name):
                current_quantity = SQL_Lookup.character_item_quantity(character_name, item_name)
                if quantity < current_quantity:
                    SQL_Update.character_item_quantity(character_name, item_name, quantity)
                    new_quantity = SQL_Lookup.character_item_quantity(character_name, item_name)
                    response_list.append("{} now has {} {}".format(character_name_list, new_quantity, item_name))
                elif quantity == current_quantity:
                    SQL_Delete.character_item(character_name, item_name)
                    response_list.append("{} now has no {}".format(character_name_list, item_name))
                character_name_list.append(character_name)

    for names in character_name_list:
        Update_Google_Roster.update_items(names)
    return "Items Updated"


def item_split(command: str):
    c_list = command.split(",")
    item_list = []
    if len(c_list) < 2:
        return False, "Please enter a character name and an item."
    # split input into names and items
    if SQL_Check.character_exists(c_list[0].lstrip()):
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

def add_item_check(command: str):  # [Character Name],[Item],[Quantity]
    c_list = command.split(",")
    if len(c_list) < 2:
        return False, "Please enter a character name and an item."
    character_name = c_list[0].lstrip()
    if SQL_Check.character_exists(character_name):
        # many items
        character_name = c_list[0].lstrip()
        del c_list[0]
        if len(c_list) == 0:
            return False, "Please enter at least one player to add an item to."
        return_list = ['Give {} the following:'.format(character_name)]
        for items in c_list:
            item_details = items.split(':')
            item_name = item_details[0].lstrip()
            try:
                quantity = int(item_details[1].lstrip())
            except IndexError:
                quantity = 1
            except ValueError:
                return False, "make sure the quantity for {} is a number".format(item_name)
            return_list.append('{} {}'.format(quantity, item_name))
        return_list.append("Do you want to continue?")
        response = Quick_Python.stitch_table(return_list)
    else:
        # many characters
        item_name = c_list[0].lstrip()
        del c_list[0]
        if len(c_list) == 0:
            return False, "Please enter at least one player to add an item to."
        return_list = ['Give {} to:'.format(item_name)]
        for characters in c_list:
            character_list = characters.split(':')
            character_name = character_list[0].lstrip()
            if not SQL_Check.character_exists(character_name):
                return False, "The character {} doesnt exist.".format(character_name)
            try:
                quantity = int(character_list[1].lstrip())
            except IndexError:
                quantity = 1
            except ValueError:
                return False, "make sure the quantity for {} is a number".format(character_name)
            return_list.append('{} gets {}'.format(character_name, quantity))
        return_list.append("Do you want to continue?")
        response = Quick_Python.stitch_table(return_list)
    return True, response


def add_item_execute(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    if SQL_Check.character_exists(character_name):
        # one character multiple items
        character_name = c_list[0].lstrip()
        del c_list[0]
        for items in c_list:
            item_details = items.split(':')
            item_name = item_details[0].lstrip()
            try:
                quantity = int(item_details[1].lstrip())
            except IndexError:
                quantity = 1
            if SQL_Check.character_has_item(character_name, item_name):
                SQL_Update.character_item_quantity(character_name, item_name, quantity)
            else:
                SQL_Insert.character_item(character_name, item_name, quantity)
        Update_Google_Roster.update_items(character_name)
    else:
        # one item multiple people
        item_name = c_list[0].lstrip()
        del c_list[0]
        for characters in c_list:
            character_list = characters.split(':')
            character_name = character_list[0].lstrip()
            try:
                quantity = int(character_list[1].lstrip())
            except IndexError:
                quantity = 1
            if SQL_Check.character_has_item(character_name, item_name):
                SQL_Update.character_item_quantity(character_name, item_name, quantity)
            else:
                SQL_Insert.character_item(character_name, item_name, quantity)
            Update_Google_Roster.update_items(character_name)
    return "Items Updated"


def remove_item_check(command: str):
    c_list = command.split(",")
    if len(c_list) < 2:
        return False, "Please enter a character name and an item."
    character_name = c_list[0].lstrip()
    item = c_list[1].split(":")
    item_name = item[0].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    try:
        quantity = int(item[1].lstrip())
    except IndexError:
        quantity = 1
    if not SQL_Check.character_has_item(character_name, item_name):
        return False, "Character doesnt own that item."
    owned_quantity = int(SQL_Lookup.character_item_quantity(character_name, item_name))
    if owned_quantity < quantity:
        return False, "{} only owns {} {}, you cannot remove {}.".format(character_name, owned_quantity,
                                                                         item_name, quantity)
    return True, "remove {} {} from {}?".format(quantity, item_name, character_name)


def remove_item_execute(command: str):
    # get inputs data
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    item = c_list[1].split(":")
    item_name = item[0].lstrip()
    try:
        quantity = int(item[1].lstrip())
    except IndexError:
        quantity = 1
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        quantity = quantity * -1
        SQL_Delete.character_item(character_name, item_name)
    else:
        quantity = quantity * -1
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    Update_Google_Roster.update_items(character_name)
    return "{} now has {} less {}".format(character_name, quantity, item_name)


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
    return True, "Give {} xp to {}?".format(xp, Quick_Python.stitch_string(c_list))


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
    return "{} xp has been added to {}".format(xp, Quick_Python.stitch_string(c_list))


def log_xp_check(character_name: str):
    if not SQL_Check.character_exists(character_name.lstrip()):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, ""


def log_xp_execute(character_name: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    if SQL_Check.level_up_check(character_name):
        character_level += 1
    xp = SQL_Lookup.log_xp(character_level)
    SQL_Update.character_xp(character_name.lstrip(), xp)
    c_list = [character_name]
    Update_Google_Roster.update_xp_group(c_list)
    user_ping = "<@{}>".format(SQL_Lookup.character_owner(character_name))
    return "{} {} got {}xp for posting a log".format(user_ping, character_name, xp)


def npc_talk_execute(command: str):
    command_split = command.split(":")
    npc = command_split[0].lstrip()
    speach = command_split[1].lstrip()
    response = "```" \
               "NPC:{}\n" \
               "{}" \
               "```".format(npc, speach)
    return response