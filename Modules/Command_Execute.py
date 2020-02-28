import Quick_Python
import Quick_Google
import SQL_Lookup
import SQL_Insert
import SQL_Delete
import SQL_Update
import SQL_Check
import Update_Google_Roster
import Update_Google_Trade

'''''''''''''''''''''''''''''''''''''''''
############DM commands#################
'''''''''''''''''''''''''''''''''''''''''


def kill_character(command: str):
    c_list = command.split(",")
    character_name = c_list[0]
    reason = c_list[1]

    SQL_Insert.move_to_graveyard(character_name.lstrip(), reason.lstrip())
    SQL_Delete.character(character_name.lstrip())
    Update_Google_Roster.kill_character(command)
    return "{} died because {}".format(character_name, reason)


def add_gold(command: str):  # [Gold],[Character 1],[Character 2]
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


def add_item(command: str):
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


def remove_item(command: str):
    # get inputs data
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()
    try:
        quantity = int(c_list[2].lstrip())
    except IndexError:
        quantity = 1
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    Update_Google_Roster.update_items(character_name)
    return "{} now has {} less {}".format(character_name, quantity, item_name)


def add_xp(command: str):  # [Gold],[Character 1],[Character 2]
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


'''''''''''''''''''''''''''''''''''''''''
#############MOD commands###############
'''''''''''''''''''''''''''''''''''''''''


def create_character(command: str):
    character_sheet = command.split(",")
    character_name = character_sheet[1].lstrip()
    character_class = character_sheet[4].lstrip()

    discord_id = SQL_Lookup.player_id_by_name(character_sheet[0].lstrip())
    character_sheet[0] = discord_id

    # update Link_character_Class
    SQL_Insert.character_create(character_sheet)
    SQL_Insert.character_class(character_name, character_class, 1, 1)
    Update_Google_Roster.insert_new_character(character_name)
    Update_Google_Roster.update_classes(character_name)
    return "{} has been created".format(character_name)


def character_sync(character_name: str):
    roster = Quick_Google.sheet("Roster")
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


def character_refresh(character_name: str):
    Update_Google_Roster.update_character(character_name)
    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_feat(character_name)
    Update_Google_Roster.update_items(character_name)


def character_update_owner(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    discord_id = c_list[1].lstrip()
    discord_name = SQL_Lookup.player_name_by_id(discord_id)
    SQL_Update.character_owner(character_name, discord_id)
    Update_Google_Roster.update_character(character_name)
    return "{} is now owned by {}".format(character_name, discord_name)


def add_feat(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()

    # get google sheet data
    SQL_Insert.character_feat(character_name, feat)
    Update_Google_Roster.update_feat(character_name)

    return "The character {} now has the feat {}".format(character_name, feat)


def remove_feat(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    feat = c_list[1].lstrip()

    SQL_Delete.character_feat(character_name, feat)
    Update_Google_Roster.update_feat(character_name)

    return "the feat {} has been removed from {}".format(feat, character_name)


def skill_add(command: str):
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


def skill_remove(command: str):
    # pull values
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    skill = c_list[1].lstrip()

    SQL_Delete.character_skill(character_name, skill)
    Update_Google_Roster.update_skill(character_name)

    return "the skill {} has been removed from {}".format(skill, character_name)


def npc_talk(command: str):
    command_split = command.split(":")
    npc = command_split[0].lstrip()
    speach = command_split[1].lstrip()
    response = "```" \
               "NPC:{}\n" \
               "{}" \
               "```".format(npc, speach)
    return response


def stat_change(command: str):
    command_split = command.split(",")
    character_name = command_split[0].lstrip()
    ability = command_split[1].lstrip()
    value = int(command_split[2].lstrip())
    new_value = SQL_Update.character_stat_change(character_name, ability, value)
    Update_Google_Roster.update_character_ability(character_name, ability)
    return "{} now has {} in {}".format(character_name, new_value, ability)


'''''''''''''''''''''''''''''''''''''''''
###########Player commands###############
'''''''''''''''''''''''''''''''''''''''''


def rand_char(discord_id: str):
    stat_array = []
    stat_display_list = []
    for rolls in range(0, 6): # Roll 6 times
        dice_results = []
        for roll_number in range(0, 4):  # Roll 4 dice
            dice = int(Quick_Python.dice_roll(1, 6))
            dice_results.append(dice)  # [6,3,2,6]
        lowest = False
        stat_display = ['(']
        for roll in dice_results:
            if roll == min(dice_results) and lowest is False:  # find the first lowest roll
                stat_display.append(['~~{}~~'.format(roll)])  # Strike through  the lowest
                lowest = True
            else:
                stat_display.append(['**{}**'.format(roll)])  # bold the rest
        # update display of stats
        total_stat = sum(dice_results) - min(dice_results)
        stat_display.append(')')  # ['(',6,3,2,6,')']
        stat_display.append(' = **{}**'.format(total_stat))  # ['(',6,3,2,6,')',' = 15' ]
        stat_display_list.append(Quick_Python.stitch_string(stat_display))  # ['(6,3,2,6) = 15']
        # save stats
        stat_array.append(total_stat)
    # save to SQL after
    # SQL_Insert.discord_roll(discord_id, stat_array)  # create new entry in discord roll
    # print to discord
    roll_total = sum(stat_array)
    stat_display_list.append('Total = {}'.format(roll_total))
    response = Quick_Python.stitch_table(stat_display_list)
    return response


def level_up(command: str):
    # get inputs data
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    character_class = c_list[1].lstrip()

    if SQL_Check.character_has_class(character_name, character_class):
        SQL_Update.character_class_level(character_name, character_class)
    else:
        number = SQL_Lookup.character_count_classes(character_name) + 1
        SQL_Insert.character_class(character_name, character_class, 1, number)

    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_level(character_name)
    total_level = SQL_Lookup.character_sum_class_levels(character_name)
    return "{} gained a level in {} and is now level {} overall".format(character_name, character_class, total_level)


def trade_sell(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()
    value = int(c_list[2])
    quantity = int(c_list[3])

    # update SQL
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    SQL_Insert.trade_sell(character_name, item_name, quantity, value)

    # update google
    Update_Google_Roster.update_items(character_name)
    Update_Google_Trade.trade_create(character_name, item_name)
    return "{} {} is now for sale at {}g each".format(quantity, item_name, value)


def trade_buy(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    seller_name = c_list[1].lstrip()
    item_name = c_list[2]
    quantity = int(c_list[3])
    item_value = SQL_Lookup.trade_item_price(seller_name, item_name)
    trade_value = item_value * quantity

    # add to player inventory
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    else:
        SQL_Insert.character_item(character_name, item_name, quantity)

    # remove gold from player
    SQL_Update.character_gold(character_name, trade_value*-1)
    # add gold to seller
    SQL_Update.character_gold(seller_name, trade_value)

    # remove from trade
    if quantity == SQL_Lookup.trade_item_quantity(seller_name, item_name):
        SQL_Delete.trade_sale(seller_name, item_name)
        Update_Google_Trade.trade_delete(seller_name, item_name)
    else:
        SQL_Update.trade_quantity(seller_name, item_name, quantity * -1)
        Update_Google_Trade.trade_update(seller_name, item_name)

    # update roster
    update_list = [character_name, seller_name]
    Update_Google_Roster.update_gold_group(update_list)
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_items(seller_name)
    return "{} bought {} {} from {} for {}g".format(character_name, quantity, item_name, seller_name, trade_value)


def trade_stop(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()
    quantity = SQL_Lookup.trade_item_quantity(character_name, item_name)

    # return to inventory
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    else:
        SQL_Insert.character_item(character_name, item_name, quantity)
    # remove trade
    SQL_Delete.trade_sale(character_name, item_name)

    Update_Google_Trade.trade_delete(character_name, item_name)
    Update_Google_Roster.update_items(character_name)
    return "{} stopped selling {}".format(character_name, item_name)


def info_skills():
    skill_list = SQL_Lookup.info_skills()
    reply = Quick_Python.stitch_string(skill_list)
    return reply


def info_classes():
    class_list = SQL_Lookup.info_classes()
    reply = Quick_Python.stitch_string(class_list)
    return reply


'''''''''''''''''''''''''''''''''''''''''
###########Utility commands##############
'''''''''''''''''''''''''''''''''''''''''


def sync_players(command: str):
    new_players = 0
    update_player = 0
    for member in command.guild.members:
        discord_name = member.display_name.replace("'", "")
        discord_id = member.id
        if not SQL_Check.player_exists(discord_id):
            SQL_Insert.sync_players(discord_id, discord_name)
            new_players += 1
        elif discord_name != SQL_Lookup.player_name_by_id(discord_id):
            SQL_Update.player_name(discord_name, discord_id)
            update_player += 1
    return "{} new players found\n{} player names updated".format(new_players, update_player)
