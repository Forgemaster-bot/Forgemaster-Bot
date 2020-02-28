import Quick_Google
import SQL_Check
import SQL_Lookup
import Quick_Python

'''''''''''''''''''''''''''''''''''''''''
############DM commands#################
'''''''''''''''''''''''''''''''''''''''''


def kill_character(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter one character and a cause of death."
    character_name = c_list[0].lstrip()
    reason = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    return True, "did {} die by {}?".format(character_name, reason)


def add_gold(command: str):  # [Gold],[Character 1],[Character 2]
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


def add_item(command: str):  # [Character Name],[Item],[Quantity]
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


def remove_item(command: str):
    c_list = command.split(",")
    if len(c_list) < 2:
        return False, "Please enter a character name and an item."
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    try:
        quantity = int(c_list[2].lstrip())
    except IndexError:
        quantity = 1
    if not SQL_Check.character_has_item(character_name, item_name):
        return False, "Character doesnt own that item."
    owned_quantity = int(SQL_Lookup.character_item_quantity(character_name, item_name))
    if owned_quantity < quantity:
        return False, "{} only owns {} {}, you cannot remove {}.".format(character_name, owned_quantity,
                                                                         item_name, quantity)
    return True, "remove {} {} from {}?".format(quantity, item_name, character_name)


def reward_xp(command: str):
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


'''''''''''''''''''''''''''''''''''''''''
###########Mod commands###############
'''''''''''''''''''''''''''''''''''''''''


def create_character(command: str):
    c_list = command.split(",")
    if len(c_list) < 12:
        return False, "You have not entered enough stats to make a character."
    if len(c_list) > 12:
        return False, "You have entered too many stats to make a character."
    discord_name = c_list[0].lstrip()
    discord_id = SQL_Lookup.player_id_by_name(c_list[0].lstrip())
    if discord_id == "":
        return False, "Player name not found, please use $SyncPlayers to refresh player list and try again."
    if SQL_Check.character_exists(c_list[1].lstrip()):
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
                     .format(discord_name, c_list[1].lstrip(), c_list[2].lstrip(),
                             c_list[3].lstrip(), c_list[4].lstrip(), c_list[5].lstrip(),
                             c_list[6].lstrip(), c_list[7].lstrip(), c_list[8].lstrip(),
                             c_list[9].lstrip(), c_list[10].lstrip(), c_list[11].lstrip())
    return response


def character_sync(character_name: str):
    roster = Quick_Google.sheet("Roster")
    character_row = Quick_Python.find_character_row(roster.col_values(2), character_name)
    if character_row == 0:
        return False, "The character {} doesnt exist.".format(character_name)
    return True, "Do you want to update the SQL database with the roster information for {}?".format(character_name)


def character_refresh(character_name: str):
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    return "T"


def character_update_owner(command: str):
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


def add_feat(command: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a feat."
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist.".format(character_name)
    if not SQL_Check.feat_exists(feat):
        return False, "The feat {} doesnt exist.".format(feat)
    return True, "Give {} the feat {}?".format(character_name, feat)


def remove_feat(command: str):
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


def skill_add(command: str):
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


def skill_remove(command: str):
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


def stat_raise(command: str):
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


'''''''''''''''''''''''''''''''''''''''''
###########Player commands###############
'''''''''''''''''''''''''''''''''''''''''


def dice_roll(command: str):
    # split message into parts
    c_list = command.split("D")
    if c_list[0] == command:
        return "Please us a capital D when rolling"
    if len(c_list) == 1:
        return "Please enter two values, first for number of dice, then for sides"


def roll_stats(discord_id: str):
    if not SQL_Check.player_exists(discord_id):
        return False, "You are not on the system, please ask a mod to use the $SyncPlayer command"
    if SQL_Check.player_stat_roll(discord_id):
        results = SQL_Lookup.player_stat_roll(discord_id)
        previous_rolls = [results.Roll_1, results.Roll_2, results.Roll_3,
                          results.Roll_4, results.Roll_5, results.Roll_6]
        response = Quick_Python.stitch_string(previous_rolls)
        return False, "You already have a stat array : {}".format(response)
    return True, ''


def level_up(command: str, discord_id: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter a character name and a class"
    character_name = c_list[0].lstrip()
    character_class = c_list[1].lstrip()

    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist".format(character_name)
    if not SQL_Check.player_owns_character(character_name, discord_id):
        return False, "You don't own the character {}.".format(character_name)
    if SQL_Check.level_up_check(character_name) == "No":
        return False, "{} doesnt have enough XP to level.".format(character_name)
    if not SQL_Check.class_exists(character_class):
        return False, "The class {} isnt on the class list.".format(character_class)
    if not SQL_Check.character_has_class(character_name, character_class):
        if SQL_Lookup.character_count_classes(character_name) > 2:
            False, "{} aleady has three classes.".format(character_name)
    # if its passed all tests its fine to level up
    return True, "Add a level of {} to {}?".format(character_class, character_name)


def trade_sell(command: str, discord_id: str):  # [Character Name],[Item Name],[Value],[Quantity]
    c_list = command.split(",")
    if len(c_list) != 4:
        return False, "Please enter your character name, the item name, the value and the quantity"

    # character
    character_name = c_list[0].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist".format(character_name)
    if not SQL_Check.player_owns_character(character_name, discord_id):
        return False, "You don't own the character {}.".format(character_name)

    # item
    item_name = c_list[1].lstrip()
    if not SQL_Check.character_has_item(character_name, item_name):
        return False, "{} doesnt own any {}".format(character_name, item_name)

    # value
    try:
        value = int(c_list[2])
    except ValueError:
        return False, "Make sure the value of the item is a number"

    # quantity
    try:
        quantity = int(c_list[3])
    except ValueError:
        return False, "Make sure the quantity is a number"
    if quantity > SQL_Lookup.character_item_quantity(character_name, item_name):
        return False, "{} doesnt own {} {} to sell".format(character_name, quantity, item_name)

    # check trade
    if SQL_Check.character_selling_item(character_name, item_name):
        return False, "{} is already selling {}, end the sale before selling more".format(character_name, item_name)

    return True, "Put up {} {} from {} for {}g each?".format(quantity, item_name, character_name, value)


def trade_buy(command: str, discord_id: str):  # [Character Name],[Seller's Name],[Item Name],[Quantity]
    c_list = command.split(",")
    if len(c_list) != 4:
        return False, "Please enter your character name, the sellers name, the item and the quantity"

    # character
    character_name = c_list[0].lstrip()
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist".format(character_name)
    if not SQL_Check.player_owns_character(character_name, discord_id):
        return False, "You don't own the character {}.".format(character_name)

    # Seller + item
    seller = c_list[1].lstrip()
    item_name = c_list[2].lstrip()
    if character_name == seller:
        return "you cant buy off yourself"
    if not SQL_Check.character_selling_item(seller, item_name):
        return False, "{} isn't selling any {}".format(seller, item_name)

    # Quantity
    try:
        quantity = int(c_list[3])
    except ValueError:
        return False, "Make sure the value of the item is a number"
    if quantity > SQL_Lookup.trade_item_quantity(seller, item_name):
        return False, "{} doesnt have enough {} for you to buy {}".format(seller, item_name, quantity)

    # cost and gold
    available_gold = SQL_Lookup.character_gold(character_name)
    item_cost = SQL_Lookup.trade_item_price(seller, item_name)
    total_cost = item_cost * quantity
    if available_gold < item_cost * quantity:
        return False, "You don't have the {}g needed to buy {} {}".format(total_cost, quantity, item_name)
    return True, "Do you want to buy {} {} from {} for {}g?".format(quantity, item_name, seller, total_cost)


def trade_stop(command: str, discord_id: str):
    c_list = command.split(",")
    if len(c_list) != 2:
        return False, "Please enter your character name, and the item to stop selling"
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()

    # character
    if not SQL_Check.character_exists(character_name):
        return False, "The character {} doesnt exist".format(character_name)
    if not SQL_Check.player_owns_character(character_name, discord_id):
        return False, "You don't own the character {}.".format(character_name)
    # item
    if not SQL_Check.character_selling_item(character_name, item_name):
        return False, "{} isn't selling any {}".format(character_name, item_name)
    return True, "Do you want to stop selling {}?".format(item_name)


'''''''''''''''''''''''''''''''''''''''''
###########Utility commands##############
'''''''''''''''''''''''''''''''''''''''''
