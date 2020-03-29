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





'''''''''''''''''''''''''''''''''''''''''
#############MOD commands###############
'''''''''''''''''''''''''''''''''''''''''


def create_character(command: str):
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
    Update_Google_Roster.update_skill(character_name)


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


def stat_change(command: str):
    command_split = command.split(",")
    character_name = command_split[0].lstrip()
    ability = command_split[1].lstrip()
    value = int(command_split[2].lstrip())
    new_value = SQL_Update.character_stat_change(character_name, ability, value)
    Update_Google_Roster.update_character_ability(character_name, ability)
    return "{} now has {} in {}".format(character_name, new_value, ability)


def roll_check(command: str):
    command_split = command.split(",")
    discord_name = command_split[0]
    discord_id = SQL_Lookup.player_id_by_name(discord_name)
    response = SQL_Lookup.player_stat_roll(discord_id)
    if response == "":
        return "Player hasnt rolled stats"
    else:
        return Quick_Python.stitch_string(response).replace("{},".format(discord_id), "{}:".format(discord_name))


'''''''''''''''''''''''''''''''''''''''''
###########Player commands###############
'''''''''''''''''''''''''''''''''''''''''


def rand_char(discord_id: str):
    stat_array = []
    stat_display_list = []
    for rolls in range(0, 6):  # Roll 6 times
        dice_results = []
        for roll_number in range(0, 4):  # Roll 4 dice
            dice = int(Quick_Python.dice_roll(1, 6))
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
        result = Quick_Python.stitch_string(stat_display).replace("),", ")")

        # save stats
        stat_array.append(total_stat)
        stat_display_list.append(result)
    # save to SQL after
    SQL_Insert.discord_roll(discord_id, stat_array)  # create new entry in discord roll
    # print to discord
    roll_total = sum(stat_array)
    stat_display_list.insert(0, "**{}:**".format(SQL_Lookup.player_name_by_id(discord_id)))
    stat_display_list.append('Total = **{}**'.format(roll_total))
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


def pay(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    receiver_name = c_list[1].lstrip()
    amount = float(c_list[2].lstrip())

    SQL_Update.character_gold(character_name, amount*-1)
    SQL_Update.character_gold(receiver_name, amount)
    Update_Google_Roster.update_gold_group([character_name, receiver_name])

    user_ping = "<@{}>".format(SQL_Lookup.character_owner(receiver_name))
    return "{} {} paid {} {}g".format(user_ping, character_name, receiver_name, amount)


def sell(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    item_name = c_list[1].lstrip()
    quantity = int(c_list[2].lstrip())
    item = SQL_Lookup.item_detail(item_name)
    total_value = (item.Value/2 * quantity)

    # update SQL
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity*-1)
    SQL_Update.character_gold(character_name, total_value)
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_gold_group([character_name])
    return "{} sold {} {} for {} to the town".format(character_name, quantity, item_name, total_value)


def trade_sell(character_name: str, item_name: str, value: float, quantity: int):
    # update SQL
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity * -1)
    SQL_Insert.trade_sell(character_name, item_name, quantity, value)

    # update google
    Update_Google_Roster.update_items(character_name)
    Update_Google_Trade.trade_create(character_name, item_name)
    return "{} {} are now up for sale at {}g each".format(quantity, item_name, value)


def trade_buy(character_name: str, seller_name: str, item_name: str, quantity: int):
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
    user_ping = "<@{}>".format(SQL_Lookup.character_owner(seller_name))
    return "{} bought {} {} from {} for {}g".format(character_name, quantity, item_name, user_ping, trade_value)


def trade_stop(character_name: str, item_name: str):
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


'''''''''''''''''''''''''''''''''''''''''
###########Utility commands##############
'''''''''''''''''''''''''''''''''''''''''


def info_skills():
    skill_list = SQL_Lookup.info_skills()
    reply = Quick_Python.stitch_string(skill_list)
    return reply


def info_classes():
    class_list = SQL_Lookup.info_classes()
    reply = Quick_Python.stitch_string(class_list)
    return reply


def sync_players(command):
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


'''''''''''''''''''''''''''''''''''''''''
################Crafting#################
'''''''''''''''''''''''''''''''''''''''''


def crafting_message(character_name):
    character_gold = SQL_Lookup.character_gold(character_name)
    craft_limit = SQL_Lookup.character_crafting_points(character_name)
    craft_points = craft_limit[1]
    craft_value = craft_limit[2]
    labour = craft_limit[3]
    labour_value = labour_crafting_value(labour)
    if craft_points > 0:
        value_message = "You haven't worked this week so you can craft {}g worth of goods, " \
                        "or you could make one valuable item.".format(craft_value)
        if labour_value > 0:
            max_message = "As you've recruited {} workers this week, the item can be worth up to {}g.".format(
                labour, labour_value)
        else:
            max_message = "As your working alone this week, the item can be worth up to 100g."
    else:
        value_message = "You've already crafted this week, you have " \
                        "{}g remaining in value of goods you can make.".format(craft_value)
        max_message = ""

    message = "Welcome {}, you have {}g that can be spent on raw materials, " \
              "{} {} Type stop at any point to stop crafting."\
        .format(character_name, character_gold, value_message, max_message)
    return message


def crafting_gold_limit(character_name: str):
    character_gold = SQL_Lookup.character_gold(character_name)
    craft_limit = SQL_Lookup.character_crafting_points(character_name)
    craft_value = craft_limit[2]/2
    labour_value = labour_crafting_value(craft_limit[3])
    if labour_value == 0:
        limit_list = [character_gold, craft_value]
        return min(limit_list)
    else:
        limit_list = [character_gold, craft_value, labour_value]
        return min(limit_list)


def labour_crafting_value(labour: int):
    if labour == 1:
        value = 500
    elif labour == 2:
        value = 5000
    elif labour > 2:
        value = 50000
    else:
        value = 0
    return value


def craft_item(character_name: str, item_name: str, quantity: int):
    item = SQL_Lookup.item_detail(item_name)
    # update gold
    craft_cost = item.Value/2 * quantity
    SQL_Update.character_gold(character_name, craft_cost * -1)
    Update_Google_Roster.update_gold_group([character_name])
    # update inventory
    add_item_command = "{},{}:{}".format(character_name, item_name, quantity)
    add_item(add_item_command)
    # update crafting
    craft_details = SQL_Lookup.character_crafting_points(character_name)
    new_craft_value = craft_details[2] - (craft_cost*2)
    if new_craft_value <= 0:
        new_craft_value = 0
    SQL_Update.crafting_points(character_name, 0, new_craft_value, 0)
    return


def work(command: str):
    c_list = command.split(",")
    character_name = c_list[0].lstrip()
    employer_name = c_list[1].lstrip()
    employer_points = SQL_Lookup.character_crafting_points(employer_name)
    new_labour = employer_points[3] + 1
    # remove point from player
    SQL_Update.crafting_points(character_name, 0, 0, 0)
    # add labour to employer
    SQL_Update.crafting_points(employer_name, 1, 100, new_labour)
    return "You are now working for {}, giving him one more labour point for the week".format(employer_name)


