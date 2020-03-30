from Player_Menu import SQL_Check
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Update
from Player_Menu import SQL_Insert
from Player_Menu import SQL_Delete
import Update_Google_Roster
import Update_Google_Trade
import random


def main_menu_options(character_name: str):
    menu_option_list = []
    # Craft
    if not SQL_Check.character_on_crafting_table(character_name):
        SQL_Insert.crafting_point(character_name)
    menu_option_list.append("Craft items")
    # Give item
    if SQL_Check.character_has_items_to_trade(character_name):
        menu_option_list.append("Give items to other characters")
    # level
    if SQL_Check.character_can_level_up(character_name):
        menu_option_list.append("Level up your character")
    # Pay
    if SQL_Check.character_has_gold(character_name):
        menu_option_list.append("Pay a character")
    # Pick a profession
    if not SQL_Check.character_has_professions(character_name):
        menu_option_list.append("Pick your free crafting profession")
    # sell
    if SQL_Check.character_has_items_to_trade(character_name):
        menu_option_list.append("Sell an item to town")
    # trade
    if SQL_Check.character_has_items_to_trade(character_name) or SQL_Check.character_has_items_on_sale(character_name):
        menu_option_list.append("Trade at the marketplace")
    # Work
    if SQL_Check.character_has_crafted_this_week(character_name):
        menu_option_list.append("Work for a character")
    # menu_option_list.append("Test")
    return menu_option_list


'''''''''''''''''''''''''''''''''''''''''
################Crafting#################
'''''''''''''''''''''''''''''''''''''''''


def craft_create_mundane_item(character_name: str, item_name: str, quantity: int):
    item = SQL_Lookup.item_detail(item_name)
    # update gold
    craft_cost = item.Value/2 * quantity
    SQL_Update.character_gold(character_name, craft_cost * -1)
    Update_Google_Roster.update_gold_group([character_name])

    # update inventory
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, quantity)
    else:
        SQL_Insert.character_item(character_name, item_name, quantity)
    Update_Google_Roster.update_items(character_name)

    # update crafting
    craft_details = SQL_Lookup.character_main_crafting(character_name)
    new_craft_value = int(craft_details[1]) - craft_cost
    if new_craft_value <= 0:
        new_craft_value = 0
    SQL_Update.character_main_crafting(character_name, new_craft_value, 0)
    return


def craft_create_experiment(character_name: str, profession: str, recipe_name: str, essence_1: str, essence_2: str):
    # learn new recipe
    SQL_Insert.character_recipe(character_name, profession, recipe_name)
    # take gold from player
    SQL_Update.character_gold(character_name, -20)

    # update crafting
    craft_details = SQL_Lookup.character_main_crafting(character_name)
    new_craft_value = int(craft_details[1]) - 20
    SQL_Update.character_main_crafting(character_name, new_craft_value, 0)

    # add item to player
    item_type = SQL_Lookup.profession_consumable_name(profession)

    # remove essences 1
    if SQL_Lookup.character_item_quantity(character_name, essence_1) == 1:
        SQL_Delete.character_item(character_name, essence_1)
    else:
        SQL_Update.character_item_quantity(character_name, essence_1, -1)

    # remove essences 2
    if SQL_Lookup.character_item_quantity(character_name, essence_2) == 1:
        SQL_Delete.character_item(character_name, essence_2)
    else:
        SQL_Update.character_item_quantity(character_name, essence_2, -1)

    # add new item to player inventory
    item_name = "{} of {}".format(item_type, recipe_name)
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, 1)
    else:
        SQL_Insert.character_item(character_name, item_name, 1)

    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_gold_group([character_name])


def craft_create_consumable(character_name: str, item_type: str, profession: str,
                            item_name: str, effect_list: list, cost: int):
    # remove gold
    SQL_Update.character_gold(character_name, - cost)

    # remove crafting value
    craft_details = SQL_Lookup.character_main_crafting(character_name)
    new_craft_value = int(craft_details[1]) - cost
    SQL_Update.character_main_crafting(character_name, new_craft_value, 0)

    # remove essences
    for effect in effect_list:
        recipe_essences_list = SQL_Lookup.recipe_essence_list(profession, effect)
        for essence in recipe_essences_list:
            if SQL_Lookup.character_item_quantity(character_name, essence) == 1:
                SQL_Delete.character_item(character_name, essence)
            else:
                SQL_Update.character_item_quantity(character_name, essence, -1)

    # add new item to player inventory
    name = "{} of {}".format(item_type, item_name)
    if SQL_Check.character_has_item(character_name, name):
        SQL_Update.character_item_quantity(character_name, name, 1)
    else:
        SQL_Insert.character_item(character_name, name, 1)

    # update
    Update_Google_Roster.update_gold_group([character_name])
    Update_Google_Roster.update_items(character_name)


def character_has_profession_tools(character_name, profession: str):
    tool = SQL_Lookup.profession_tool(profession)
    if SQL_Check.character_has_class(character_name, "Artificer"):
        artificer_level = SQL_Lookup.character_class_level_by_class(character_name, "Artificer")
        if artificer_level > 2 and SQL_Check.character_has_item(character_name, "Tinker tools"):
            return True, ""
    if not SQL_Check.character_has_item(character_name, tool):
        return False, "{} doesnt own a set of {} to craft with".format(character_name, tool)
    return True, ""


def crafting_gold_limit(character_name: str):
    character_gold = SQL_Lookup.character_gold_total(character_name) * 2
    craft_limit = SQL_Lookup.character_main_crafting(character_name)
    craft_value = craft_limit[1]
    labour_value = labour_crafting_value(craft_limit[2])
    if labour_value == 0:
        limit_list = [character_gold, craft_value]
        return min(limit_list)
    else:
        limit_list = [character_gold, labour_value]
        return min(limit_list)


def crafting_welcome_message(character_name):
    character_gold = SQL_Lookup.character_gold_total(character_name)
    craft_limit = SQL_Lookup.character_main_crafting(character_name)
    craft_value = int(craft_limit[1])
    labour = craft_limit[2]
    labour_value = labour_crafting_value(labour) * 2

    value_message = "You can spend {}g on materials this week.".format(craft_value)

    if labour_value > 0 and craft_value == 50:
        max_message = "As you've recruited {} workers this week, You can instead make one item up to {}g."\
            .format(labour, labour_value)
    elif craft_value == 50:
        max_message = "You haven't recruited any workers so you cant build anything larger."
    else:
        max_message = ""
    message = "Craft Menu: Type **STOP** at any time to go back to the player menu \n" \
              "You have {}g. {} {} "\
        .format(character_gold, value_message, max_message)
    return message


def labour_crafting_value(labour: int):
    if labour == 1:
        value = 250
    elif labour == 2:
        value = 2500
    elif labour > 2:
        value = 25000
    else:
        value = 0
    return value


def craft_essence_list(character_name: str, profession: str):
    # get lists
    known_recipes = SQL_Lookup.character_known_recipe(character_name, profession)
    profession_recipes = SQL_Lookup.recipe_by_profession(profession)
    
    # get list of unknown recipes
    for recipe in known_recipes:
        profession_recipes.remove(recipe)

    # get a list of essences needed that the player owns
    essence_list = []
    for recipe in profession_recipes:
        recipe_essence = SQL_Lookup.recipe_essence_list(profession, recipe)
        if recipe_essence[0] == recipe_essence[1]:
            if SQL_Check.character_has_item_quantity(character_name, recipe_essence[0], 2):
                if recipe_essence[0] not in essence_list:
                    essence_list.append(recipe_essence[0])
        else:
            if SQL_Check.character_has_item_quantity(character_name, recipe_essence[0], 1):
                if SQL_Check.character_has_item_quantity(character_name, recipe_essence[1], 1):
                    if recipe_essence[0] not in essence_list:
                        essence_list.append(recipe_essence[0])
                    if recipe_essence[1] not in essence_list:
                        essence_list.append(recipe_essence[1])

    for row in range(len(essence_list)):
        quantity = SQL_Lookup.character_item_quantity(character_name, essence_list[row])
        if quantity > 1:
            essence_list[row] = "{} ({})".format(essence_list[row], quantity)
    return essence_list


def craft_possible_essence_combination_list(character_name: str, profession: str, essence: str):
    known_recipes = SQL_Lookup.character_known_recipe(character_name, profession)
    profession_recipes = SQL_Lookup.recipe_by_profession(profession)

    # get list of recipes using essence
    unknown_list = []
    for recipe in profession_recipes:
        recipe_essence = SQL_Lookup.recipe_essence_list(profession, recipe)
        if recipe_essence[0] == essence or recipe_essence[1] == essence:
            unknown_list.append(recipe)

    # get list of unknown recipes using essence
    for recipe in known_recipes:
        if recipe in unknown_list:
            unknown_list.remove(recipe)

    # get list of essences that could be combined for new recipes
    essence_list = []
    for recipe in unknown_list:
        recipe_essence = SQL_Lookup.recipe_essence_list(profession, recipe)
        if recipe_essence[0] == essence:
            if recipe_essence[1] not in essence_list:
                essence_list.append(recipe_essence[1])
        else:
            if recipe_essence[0] not in essence_list:
                essence_list.append(recipe_essence[0])

    # get quantity of each essence and return
    result_list = []
    for row in range(len(essence_list)):
        if SQL_Check.character_has_item(character_name, essence_list[row]):
            quantity = SQL_Lookup.character_item_quantity(character_name, essence_list[row])
            if essence_list[row] == essence:
                quantity -= 1
            if quantity > 0:
                result_list.append("{} ({})".format(essence_list[row], quantity))
    return result_list


def craft_remove_essence_from_list(essence_list: list, essence: str):
    for row in range(len(essence_list)):
        essence_detail = essence_list[row].replace(")", "").split(" (")
        if essence_detail[0] == essence:
            if len(essence_detail) == 1:
                essence_list.remove(essence_list[row])
            elif essence_detail[1] == "2":
                essence_list[row] = essence_detail[0]
            else:
                essence_list[row] = "{} ({})".format(essence_detail[0], int(essence_detail[1])-1)
            return essence_list


def craft_recipe_list(character_name: str, profession: str, inventory_essence: list):
    known_list = SQL_Lookup.character_known_recipe(character_name, profession)

    craft_list = []
    for recipe in known_list:
        recipe_essence = SQL_Lookup.recipe_essence_and_description_list(profession, recipe)
        if recipe_essence[0] == recipe_essence[1]:
            for row in range(len(inventory_essence)):
                essence_details = inventory_essence[row].replace(")", "").split(" (",)
                if essence_details[0] == recipe_essence[0] and len(essence_details) > 1:
                    if int(essence_details[1]) > 2:
                        craft_list.append("{} : {} : **{}** + **{}**".format(recipe, recipe_essence[2],
                                                                             recipe_essence[0], recipe_essence[1]))

        else:
            for row_1 in range(len(inventory_essence)):
                essence_details_1 = inventory_essence[row_1].replace(")", "").split(" (", )
                if essence_details_1[0] == recipe_essence[0]:
                    for row_2 in range(len(inventory_essence)):
                        essence_details_2 = inventory_essence[row_2].replace(")", "").split(" (", )
                        if essence_details_2[0] == recipe_essence[1]:
                            craft_list.append(
                                "{} : {} : **{}** + **{}**".format(recipe, recipe_essence[2],
                                                                   recipe_essence[0], recipe_essence[1]))
    return craft_list


def craft_merge_effects(effect_list):
    unique_effect_list = []

    for effect in effect_list:
        if effect not in unique_effect_list:
            unique_effect_list.append(effect)

    for row in range(len(unique_effect_list)):
        quantity = effect_list.count(unique_effect_list[row])
        if quantity > 1:
            unique_effect_list[row] = "{} x {}".format(unique_effect_list[row], quantity)

    return unique_effect_list


'''''''''''''''''''''''''''''''''''''''''
################Gifting##################
'''''''''''''''''''''''''''''''''''''''''


def give_item(character_name: str, target_name: str, item_name: str, quantity: int):
    # Remove from character
    if quantity == SQL_Lookup.character_item_quantity(character_name, item_name):
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity * -1)

    # Add to target
    if SQL_Check.character_has_item(target_name, item_name):
        SQL_Update.character_item_quantity(target_name, item_name, quantity)
    else:
        SQL_Insert.character_item(target_name, item_name, quantity)

    # update roster
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_items(target_name)
    return


'''''''''''''''''''''''''''''''''''''''''
###############Leveling##################
'''''''''''''''''''''''''''''''''''''''''


def level_up(character_name: str, character_class: str):
    # get inputs data
    if SQL_Check.character_has_class(character_name, character_class):
        SQL_Update.character_class_level(character_name, character_class)
    else:
        number = SQL_Lookup.character_count_classes(character_name) + 1
        SQL_Insert.character_class(character_name, character_class, 1, number)

    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_level(character_name)
    return


'''''''''''''''''''''''''''''''''''''''''
#################Pay#####################
'''''''''''''''''''''''''''''''''''''''''


def give_gold(character_name: str, receiver_name: str, amount: float):
    SQL_Update.character_gold(character_name, amount*-1)
    SQL_Update.character_gold(receiver_name, amount)
    Update_Google_Roster.update_gold_group([character_name, receiver_name])
    return


'''''''''''''''''''''''''''''''''''''''''
#################Pay#####################
'''''''''''''''''''''''''''''''''''''''''


def give_profession(character_name: str, profession_name: str):
    # get inputs data
    SQL_Insert.character_profession(character_name, profession_name, 1)
    Update_Google_Roster.update_skill(character_name)
    return


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
##############Sell Item##################
'''''''''''''''''''''''''''''''''''''''''


def sell_item_to_town(character_name: str, item_name: str, quantity: int):
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
    return


'''''''''''''''''''''''''''''''''''''''''
#################Trade###################
'''''''''''''''''''''''''''''''''''''''''


def character_trade_options(character_name: str):
    options = []
    if SQL_Check.character_has_gold(character_name):
        options.append("Buy")
    if SQL_Check.character_has_items_to_trade(character_name):
        options.append("Sell")
    if SQL_Check.character_has_items_on_sale(character_name):
        options.append("Stop trading")
    return options


def trade_buy(character_name: str, trade_good, quantity: int):
    trade_value = trade_good.Price * quantity

    # add to player inventory
    if SQL_Check.character_has_item(character_name, trade_good.Item):
        SQL_Update.character_item_quantity(character_name, trade_good.Item, quantity)
    else:
        SQL_Insert.character_item(character_name, trade_good.Item, quantity)

    # remove gold from player
    SQL_Update.character_gold(character_name, trade_value*-1)
    # add gold to seller
    SQL_Update.character_gold(trade_good.Character, trade_value)

    # remove from trade
    if quantity == trade_good.Quantity:
        SQL_Delete.trade_sale(trade_good.Character, trade_good.Item)
        Update_Google_Trade.trade_delete(trade_good.Character, trade_good.Item)
    else:
        SQL_Update.trade_quantity(trade_good.Character, trade_good, quantity * -1)
        Update_Google_Trade.trade_update(trade_good.Character, trade_good.Item)

    # update roster
    update_list = [character_name, trade_good.Character]
    Update_Google_Roster.update_gold_group(update_list)
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_items(trade_good.Character)
    return


def trade_sell(character_name: str, item_name: str, quantity: int, value: float):
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


def trade_stop(character_name: str, item_name: str):
    trade_good = SQL_Lookup.trade_item_sold_by_character(character_name, item_name)

    # return to inventory
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, trade_good.Quantity)
    else:
        SQL_Insert.character_item(character_name, item_name, trade_good.Quantity)
    # remove trade
    SQL_Delete.trade_sale(character_name, item_name)

    Update_Google_Trade.trade_delete(character_name, item_name)
    Update_Google_Roster.update_items(character_name)
    return "{} stopped selling {}".format(character_name, item_name)


'''''''''''''''''''''''''''''''''''''''''
#################Work####################
'''''''''''''''''''''''''''''''''''''''''


def work(character_name: str, employer_name):
    employer_details = SQL_Lookup.character_main_crafting(employer_name)
    if employer_details is None:
        SQL_Insert.crafting_point(employer_name)
        new_labour = 1
        new_craft_value = 50
    else:
        new_labour = employer_details.Labour_Points + 1
        new_craft_value = employer_details.Crafting_Value
    # remove point from player
    SQL_Update.character_main_crafting(character_name, 0, 0)
    # add labour to employer
    SQL_Update.character_main_crafting(employer_name, new_craft_value, new_labour)
    return "You are now working for {}, giving him one more labour point for the week".format(employer_name)


'''''''''''''''''''''''''''''''''''''''''
################Utility##################
'''''''''''''''''''''''''''''''''''''''''


def question_list(give_list: list):
    return_string = ""
    list_length = len(give_list)
    for entry in range(list_length):
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
        if not SQL_Check.player_exists(discord_id):
            SQL_Insert.sync_players(discord_id, discord_name)
            return True, "New"
        elif discord_name != SQL_Lookup.player_name_by_id(discord_id):
            SQL_Update.player_name(discord_name, discord_id)
            return True, "Update"
    except:
        return False, "Something went wrong adding {} to the list".format(discord_name)
    return False, "No change"
