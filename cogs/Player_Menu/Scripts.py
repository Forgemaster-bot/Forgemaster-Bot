from Player_Menu import SQL_Check
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Update
from Player_Menu import SQL_Insert
from Player_Menu import SQL_Delete
import Update_Google_Roster
import Update_Google_Trade


def main_menu_options(character_name: str):
    menu_option_list = []
    # Craft
    if not SQL_Check.character_on_crafting_table(character_name):
        SQL_Insert.crafting_point(character_name)
    if SQL_Check.character_can_craft(character_name, crafting_gold_limit(character_name)):
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
    # sell
    if SQL_Check.character_has_items_to_trade(character_name):
        menu_option_list.append("Sell an item to town")
    # trade
    if SQL_Check.character_has_items_to_trade(character_name) or SQL_Check.character_has_items_on_sale(character_name):
        menu_option_list.append("Trade at the marketplace")
    # Work
    if SQL_Check.character_has_crafting_point(character_name):
        menu_option_list.append("Work for a character")
    # menu_option_list.append("Test")
    return menu_option_list


'''''''''''''''''''''''''''''''''''''''''
################Crafting#################
'''''''''''''''''''''''''''''''''''''''''


def craft_item(character_name: str, item_name: str, quantity: int):
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
    new_craft_value = craft_details[2] - (craft_cost*2)
    if new_craft_value <= 0:
        new_craft_value = 0
    SQL_Update.character_main_crafting(character_name, 0, new_craft_value, 0)
    return


def crafting_gold_limit(character_name: str):
    character_gold = SQL_Lookup.character_gold_total(character_name) * 2
    craft_limit = SQL_Lookup.character_main_crafting(character_name)
    craft_value = craft_limit[2]/2
    labour_value = labour_crafting_value(craft_limit[3])
    if labour_value == 0:
        limit_list = [character_gold, craft_value]
        return min(limit_list)
    else:
        limit_list = [character_gold, labour_value]
        return min(limit_list)


def crafting_welcome_message(character_name):
    character_gold = SQL_Lookup.character_gold_total(character_name)
    craft_limit = SQL_Lookup.character_main_crafting(character_name)
    craft_points = craft_limit[1]
    craft_value = craft_limit[2]
    labour = craft_limit[3]
    labour_value = labour_crafting_value(labour) * 2
    if craft_points == 1:
        value_message = "You haven't worked this week so you can craft {}g worth of goods.".format(craft_value)
        if labour_value > 0:
            max_message = "As you've recruited {} workers this week, You can instead make one item up to {}g.".format(
                labour, labour_value)
        else:
            max_message = "You haven't recruited any workers so you cant build anything larger."
    else:
        value_message = "You've already crafted this week, you have " \
                        "{}g remaining in value of goods you can make.".format(craft_value)
        max_message = ""

    message = "Craft Menu: Type STOP at any time to go back to the player menu \n" \
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
        SQL_Update.trade_quantity(trade_good.Character, trade_good.Item, quantity * -1)
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
    trade_good = SQL_Lookup.trade_item_details(character_name, item_name)

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
    new_labour = employer_details.Labour_Points + 1
    # remove point from player
    SQL_Update.crafting_points(character_name, 0, 0, 0)
    # add labour to employer
    SQL_Update.crafting_points(employer_name, 1, 100, new_labour)
    return "You are now working for {}, giving him one more labour point for the week".format(employer_name)


'''''''''''''''''''''''''''''''''''''''''
################Utility##################
'''''''''''''''''''''''''''''''''''''''''


async def log_to_discord(self, log: str):
    log_channel = self.bot.get_channel(689614915253567564)
    await log_channel.send(log)


def question_list(give_list: list):
    return_string = ""
    list_length = len(give_list)
    for entry in range(list_length):
        if return_string == "":
            return_string = "{} : {}".format(entry + 1, give_list[entry])
        else:
            return_string = "{}\n{} : {}".format(return_string, entry + 1, give_list[entry])
    return return_string


def stitch_string(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}, {}".format(return_string, element)
    return return_string
