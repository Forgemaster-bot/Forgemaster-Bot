from Player_Menu.Market_Menu import SQL_Lookup
from Player_Menu.Market_Menu import SQL_Delete
from Player_Menu.Market_Menu import SQL_Insert
from Player_Menu.Market_Menu import SQL_Update
from Player_Menu.Market_Menu import SQL_Check
import Quick_Python
import Connections
import Update_Google_Roster
import Update_Google_Trade


def menu(character_name: str):
    menu_list = ["Buy items",
                 "Sell items",
                 "Stop selling an item",
                 "Give an item to someone",
                 "Give gold to someone",
                 "Recycle an item"
                 ]
    if SQL_Check.character_is_wizard(character_name):
        menu_list.append("Share a spell from your spell book with someone")
    return menu_list


def character_info(character_name: str):
    character_list = []
    # inventory as string
    item_list = SQL_Lookup.character_inventory(character_name)
    character_list.append("**Inventory:** {}".format(Quick_Python.list_to_string(item_list)))
    # Gold
    gold = SQL_Lookup.character_gold(character_name)
    character_list.append("**Gold:** {}g".format(gold))

    return Quick_Python.list_to_table(character_list)


'''''''''''''''''''''''''''''''''''''''''
################Gifting##################
'''''''''''''''''''''''''''''''''''''''''


def give_character_inventory(character_name: str):
    result = SQL_Lookup.character_inventory(character_name)
    return result


def give_quantity(character_name: str, item_name: str):
    result = SQL_Lookup.character_item(character_name, item_name)
    return result.Quantity


async def give_confirm(self, discord_id, character_name: str, target_name: str, item_name: str, quantity: int, log):
    # Remove from character
    character_item_quantity = SQL_Lookup.character_item(character_name, item_name)
    if quantity == character_item_quantity.Quantity:
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

    # update logs
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
    if target_discord is not None:
        await target_discord.send(log)

'''''''''''''''''''''''''''''''''''''''''
################Paying##################
'''''''''''''''''''''''''''''''''''''''''


def pay_character_gold(character_name: str):
    result = SQL_Lookup.character_gold(character_name)
    return result


async def pay_confirm(self, discord_id, character_name: str, target_name: str, amount: float, log):
    SQL_Update.character_gold(character_name, amount*-1)
    SQL_Update.character_gold(target_name, amount)
    Update_Google_Roster.update_gold_group([character_name, target_name])

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
    if target_discord is not None:
        await target_discord.send(log)


'''''''''''''''''''''''''''''''''''''''''
################Recycle##################
'''''''''''''''''''''''''''''''''''''''''


def recycle_inventory(character_name: str):
    result = SQL_Lookup.character_recycle_inventory_list(character_name)
    return result


def recycle_character_item(character_name: str, item_name: str):
    result = SQL_Lookup.character_item(character_name, item_name)
    return result


def recycle_item_details(item_name: str):
    result = SQL_Lookup.item_detail(item_name)
    return result


async def recycle_confirm(self, discord_id, character_name: str, item_name: str, quantity: int, log):
    item_details = SQL_Lookup.item_detail(item_name)
    total_value = (item_details.Value/2) * quantity
    character_item = SQL_Lookup.character_item(character_name, item_name)
    # update SQL
    if quantity == character_item.Quantity:
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity*-1)
    SQL_Update.character_gold(character_name, total_value)
    Update_Google_Roster.update_items(character_name)
    Update_Google_Roster.update_gold_group([character_name])

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
################Buying##################
'''''''''''''''''''''''''''''''''''''''''


def buy_character_gold(character_name: str):
    result = SQL_Lookup.character_gold(character_name)
    return result


def buy_can_afford_to_buy(gold_limit: float):
    result = SQL_Check.character_has_enough_gold_to_buy_trade(gold_limit)
    return result


def buy_item_types(character_name: str, gold_limit: float):
    result = SQL_Lookup.trade_goods_types(character_name, gold_limit)
    return result


def buy_item_list(character_name: str, gold_limit: float, item_type: str):
    result = SQL_Lookup.trade_goods_items_by_type(character_name, gold_limit, item_type)
    return result


def buy_cheapest_item(item_type: str):
    result = SQL_Lookup.trade_item_cheapest_on_sale(item_type)
    return result


async def buy_confirm(self, discord_id, character_name: str, trade_good, quantity: int, log):
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

    # update logs
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    target_discord = self.bot.get_user(SQL_Lookup.character_owner(trade_good.Character))
    if target_discord is not None:
        await target_discord.send(log)


'''''''''''''''''''''''''''''''''''''''''
################Selling##################
'''''''''''''''''''''''''''''''''''''''''


def sell_inventory(character_name: str):
    result = SQL_Lookup.character_inventory(character_name)
    return result


def sell_character_item(character_name: str, item_name: str):
    result = SQL_Lookup.character_item(character_name, item_name)
    return result


async def sell_confirm(self, discord_id, character_name: str, item_name: str, quantity: int, value: float, log):
    # find item type
    item_details = SQL_Lookup.item_detail(item_name)
    if item_details is not None:
        item_type = item_details.Type
    else:
        if item_name.find(" ") != -1:
            type_list = ['Potion', 'Scroll', 'Glyph', 'Bomb', 'Snack']
            item_details = item_name[:item_name.find(" ")]
            for row in type_list:
                if item_details == row:
                    item_type = row
                    break
        item_type = "Other"

    # update SQL
    character_item_details = SQL_Lookup.character_item(character_name, item_name)
    if quantity == character_item_details.Quantity:
        SQL_Delete.character_item(character_name, item_name)
    else:
        SQL_Update.character_item_quantity(character_name, item_name, quantity * -1)

    SQL_Insert.trade_sell(character_name, item_name, quantity, value, item_type)

    # update google
    Update_Google_Roster.update_items(character_name)
    Update_Google_Trade.trade_create(character_name, item_name)

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
################Stop Sale################
'''''''''''''''''''''''''''''''''''''''''


def stop_sale_items(character_name: str):
    result = SQL_Lookup.character_items_for_sale(character_name)
    return result


async def stop_sale_confirm(self, discord_id, character_name: str, item_name: str, log):
    trade_good = SQL_Lookup.trade_item__character(character_name, item_name)

    # return to inventory
    if SQL_Check.character_has_item(character_name, item_name):
        SQL_Update.character_item_quantity(character_name, item_name, trade_good.Quantity)
    else:
        SQL_Insert.character_item(character_name, item_name, trade_good.Quantity)
    # remove trade
    SQL_Delete.trade_sale(character_name, item_name)

    Update_Google_Trade.trade_delete(character_name, item_name)
    Update_Google_Roster.update_items(character_name)

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
##############share spell################
'''''''''''''''''''''''''''''''''''''''''


def share_spell_level_options(character_name: str):
    result = SQL_Lookup.character_spell_level_list_spell_book(character_name)
    return result


def share_spell_options(character_name: str, spell_level: int):
    result = SQL_Lookup.character_known_wizard_spells_by_level(character_name, spell_level)
    return result


async def share_spell_confirm(self, discord_id, character_name: str, target_name: str, spell_name: str, log):
    SQL_Insert.share_spell(character_name, target_name, spell_name)

    # inform target
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
    if target_discord is not None:
        await target_discord.send(log)
