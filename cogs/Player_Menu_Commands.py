from discord.ext import commands
import asyncio

import Quick_SQL
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Check
from Player_Menu import Scripts


class Player_Menu_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Menu
    @commands.command(name='Menu', help="in development DONT USE")
    async def player_menu(self, command):
        discord_id = command.message.author.id
        # welcome message
        welcome = "Welcome to the Lost World player menu, to navigate around the menu " \
                  "type the option number into chat. Type **EXIT** at any time to close the menu"
        await command.message.author.send(welcome)
        # character choice
        character_name = await self.character_choice(command, discord_id)
        if character_name.lower() == "exit" or character_name.lower() == "back":
            await command.message.author.send("Menu closed")
            return
        while True:
            menu_option = await self.menu_choice(command, character_name)
            if menu_option == "Craft items":
                while True:
                    menu = await self.craft_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Give items to other characters":
                while True:
                    menu = await self.give_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Level up your character":
                while True:
                    menu = await self.level_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Pay a character":
                while True:
                    menu = await self.pay_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Sell an item to town":
                while True:
                    menu = await self.sell_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Trade at the marketplace":
                while True:
                    menu = await self.trade_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Work for a character":
                while True:
                    menu = await self.sell_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            if menu_option == "exit":
                break
        await command.message.author.send("Menu closed")

    # Menu commands
    async def character_choice(self, command, discord_id):
        option_list = SQL_Lookup.player_character_list(discord_id)
        if len(option_list) == 0:
            await command.message.author.send("You dont have any characters yet.")
            choice = "stop"
        else:
            option_question = "Which character would you like to view the menu for?"
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def menu_choice(self, command, character_name):
        option_list = Scripts.main_menu_options(character_name)
        if len(option_list) == 0:
            await command.message.author.send("{} doesnt have any options available".format(character_name))
            choice = "stop"
        else:
            option_question = "Main Menu: Welcome {}, What would you like to do? Type **EXIT** to close the menu"\
                .format(character_name)
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    # Crafting
    async def craft_menu(self, command, discord_id, character_name):
        while True:
            await command.message.author.send(Scripts.crafting_welcome_message(character_name))
            gold_limit = Scripts.crafting_gold_limit(character_name)
            profession = await self.craft_step_1_profession_choice(command, character_name, gold_limit)
            if profession == "exit" or profession == "stop":
                return profession
            craft_type_choice = await self.craft_step_2_type_choice(command, profession)
            if craft_type_choice == "Mundane item":
                # get the type of item they want to craft
                item_type = await self.craft_mundane_step_1_type_choice(command, profession, gold_limit)
                if item_type == "exit" or item_type == "stop":
                    return item_type
                # get the name of the item
                item_name = await self.craft_mundane_step_2_item_choice(command, profession, gold_limit, item_type)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                # get the quantity
                quantity = await self.craft_mundane_step_3_quantity(command, gold_limit, item_name)
                if quantity == "exit" or quantity == "stop":
                    return quantity
                # confirm crafting
                confirm = await self.craft_mundane_step_4_confirm(command, discord_id, character_name,
                                                                  item_name, quantity)
                if confirm == "exit" or confirm == "stop":
                    return confirm
                # check if they want to craft something else
                repeat = await self.craft_mundane_step_5_repeat(command)
                if repeat == "exit" or repeat == "stop":
                    return repeat
                return
            elif craft_type_choice == "Craft a consumable from a recipe":
                await command.author.send("consumable crafting is still in development, come back later")
                return
            elif craft_type_choice == "Experiment with ingredients":
                await command.author.send("consumable crafting is still in development, come back later")
                return

    async def craft_step_1_profession_choice(self, command, character_name, gold_limit):
        # collect information about how much crafting can be done
        option_list = SQL_Lookup.character_profession_list(character_name, gold_limit)
        option_question = "Please enter the number of the profession to use"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_step_2_type_choice(self, command, skill):
        # find crafting types, choose if more than one
        option_list = SQL_Lookup.profession_craft_options(skill)
        option_question = "What sort of work do you want to do as a {}?".format(skill)
        if len(option_list) == 1:
            choice = option_list[0]
        else:
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_1_type_choice(self, command, profession, gold_limit):
        option_list = SQL_Lookup.profession_item_type_list(profession, gold_limit)
        option_question = "What type of item do you want to craft?".format(profession)
        if len(option_list) == 1:
            choice = option_list[0]
        else:
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_2_item_choice(self, command, profession, gold_limit, item_type):
        option_list = SQL_Lookup.profession_item_list(profession, item_type, gold_limit)
        option_question = "What item do you want to craft?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_3_quantity(self, command, gold_limit, item_name):
        item_craft_cost = SQL_Lookup.item_value(item_name)/2
        maximum = int(gold_limit / item_craft_cost)
        if item_craft_cost > 50 or maximum == 1:
            choice = 1
        else:
            quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                                "you can make up to {}. How many would you like to make?" \
                .format(item_craft_cost, item_name, maximum)
            choice = await self.answer_with_int_number(command, quantity_question, maximum)
        return choice

    async def craft_mundane_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        item_craft_cost = SQL_Lookup.item_value(item_name) / 2
        total_cost = item_craft_cost * quantity
        await command.author.send("Do you want to craft {} {} for {}g? [yes/no]"
                                  .format(quantity, item_name, total_cost))
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("crafting..")
            log = "{} made {} {} for {}g".format(character_name, quantity, item_name, total_cost)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.craft_item(character_name, item_name, quantity)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
            return
        return "stop"

    async def craft_mundane_step_5_repeat(self, command):
        await command.author.send("Do you want to continue crafting? [yes/no]")
        choice = await self.confirm(command)
        if choice == "No":
            choice = "stop"
        return choice

    # Giving items
    async def give_menu(self, command, discord_id, character_name):
        welcome_message = "Gift Menu: Type **STOP** at any time to go back to the player menu"
        await command.message.author.send(welcome_message)
        while True:
            # get character item is being sent to
            target_name = await self.give_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name

            # get the item they want to send
            item_name = await self.give_step_2_item_choice(command, character_name, target_name)
            if item_name == "exit" or item_name == "stop":
                return item_name

            # get the quantity
            quantity = await self.give_step_3_quantity_choice(command, character_name, item_name, target_name)
            if quantity == "exit" or quantity == "stop":
                return quantity

            # confirm the gift
            confirm = await self.give_step_4_confirm(command, discord_id, character_name,
                                                     item_name, quantity, target_name)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def give_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to give items to"
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def give_step_2_item_choice(self, command, character_name, target):
        option_list = SQL_Lookup.character_inventory(character_name)
        option_question = "Please choose which item you want to give to {}".format(target)
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(" (")
        item_name = choice_details[0]
        return item_name

    async def give_step_3_quantity_choice(self, command, character_name, item_name, target_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "you own {} {}, how many do you want to give to {}?" .format(maximum, item_name,
                                                                                           target_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def give_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int, target_name):
        question = "Do you want to give {} {} {} from {} inventory?".format(target_name, quantity,
                                                                            item_name, character_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Giving...")
            log = "{} gave {} {} {}".format(character_name, target_name, quantity, item_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.give_item(character_name, target_name, item_name, quantity)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Leveling up

    async def level_menu(self, command, discord_id, character_name):
        character_levels = Scripts.stitch_string(SQL_Lookup.character_class_and_levels(character_name))
        welcome_message = "Level Menu: Type **STOP** at any time to go back to the player menu " \
                          "\n{} is currently a {}".format(character_name, character_levels)
        await command.message.author.send(welcome_message)
        while True:
            class_choice = await self.level_step_1_class_choice(command, character_name)
            if class_choice == "exit" or class_choice == "stop":
                return class_choice
            confirm = await self.level_step_2_confirm(command, discord_id, character_name, class_choice)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def level_step_1_class_choice(self, command, character_name):
        class_number = SQL_Lookup.character_count_classes(character_name)
        if class_number > 2:
            option_list = SQL_Lookup.character_class_list(character_name)
        else:
            option_list = SQL_Lookup.info_classes()
        option_question = "Which class would you like to gain a level in?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def level_step_2_confirm(self, command, discord_id, character_name, class_choice):
        question = "Do you want {} to gain a level in {}?".format(character_name, class_choice)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("leveling...")
            log = "{} gained a level in {}".format(character_name, class_choice)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.level_up(character_name, class_choice)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    # Pay Character

    async def pay_menu(self, command, discord_id, character_name):
        welcome_message = "Pay Menu: Type **STOP** at any time to go back to the player menu \n" \
                          "You can pay other players directly for goods and services"
        await command.message.author.send(welcome_message)
        while True:
            # get character item is being sent to
            target_name = await self.pay_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name
            # get quantity
            quantity = await self.pay_step_2_quantity(command, character_name, target_name)
            if quantity == "exit" or quantity == "stop":
                return quantity
            reason = await self.pay_step_3_reason(command, target_name)
            if reason == "exit" or reason == "stop":
                return reason
            # confirm the transaction
            confirm = await self.pay_step_4_confirm(command, discord_id, character_name, quantity, target_name, reason)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def pay_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to pay"
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def pay_step_2_quantity(self, command, character_name, target_name):
        maximum = SQL_Lookup.character_gold_total(character_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "you have {}g, how much do you want to give {}?" .format(maximum, target_name)
            choice = await self.answer_with_float_number(command, choice_question, maximum)
        return choice

    async def pay_step_3_reason(self, command, target_name):
        question = "Why are you paying {}?" .format(target_name)
        await command.author.send(question)
        choice = await self.answer_with_statement(command)
        return choice

    async def pay_step_4_confirm(self, command, discord_id, character_name, quantity: float, target_name, reason):
        question = "Do you want to give {} {}g because: {}?".format(target_name, quantity, reason)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Paying...")
            log = "{} gave {} {}g because: {}".format(character_name, target_name, quantity, reason)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.give_gold(character_name, target_name, quantity)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Sell Item to town
    async def sell_menu(self, command, discord_id, character_name):
        welcome_message = "Sell Menu: Type **STOP** at any time to go back to the player menu \n" \
                          "You can sell mundane items to the town at their crafting value"
        await command.message.author.send(welcome_message)
        while True:
            # get the item they want to sell
            item_name = await self.sell_step_1_item_choice(command, character_name)
            if item_name == "exit" or item_name == "stop":
                return item_name

            # get the quantity
            quantity = await self.sell_step_2_quantity_choice(command, character_name, item_name)
            if quantity == "exit" or quantity == "stop":
                return quantity

            # confirm sale
            confirm = await self.sell_step_3_confirm(command, discord_id, character_name, item_name, quantity)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def sell_step_1_item_choice(self, command, character_name,):
        option_list = SQL_Lookup.character_sellable_inventory_list(character_name)
        option_question = "Please choose which item you want to sell?"
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(" (")
        item_name = choice_details[0]
        return item_name

    async def sell_step_2_quantity_choice(self, command, character_name, item_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        item_value = SQL_Lookup.item_value(item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "{} sell for {} each, you own {}, how many do you want to sell?"\
                .format(item_name, item_value, maximum, item_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def sell_step_3_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        item_value = SQL_Lookup.item_value(item_name)
        total_value = item_value * quantity
        question = "Do you want to sell {} {} for {}g each for a total of {}g?"\
            .format(quantity, item_name, item_value, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} sold {} {} for {}g".format(character_name, quantity, item_name, total_value)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.sell_item_to_town(character_name, item_name, quantity)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    # Trade item in market
    async def trade_menu(self, command, discord_id, character_name):
        while True:
            welcome_message = "Trade Menu: Type **STOP** at any time to go back to the player menu \n" \
                              "You can buy and sell anything in your inventory to other members of town"
            await command.message.author.send(welcome_message)
            trade_type = await self.trade_step_1_choice(command, character_name)
            if trade_type == "exit" or trade_type == "stop":
                return trade_type
            elif trade_type == "Buy":
                gold_limit = SQL_Lookup.character_gold_total(character_name)
                # what item type are they looking for?
                item_type = await self.trade_buy_step_1_item_type_choice(command, gold_limit, character_name)
                if item_type == "exit" or item_type == "stop":
                    return item_type
                # what item do they want?
                item_name = await self.trade_buy_step_2_item_choice(command, gold_limit, item_type, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                # how many do they want to buy?
                quantity = await self.trade_buy_step_3_quantity(command, character_name, item_name)
                if quantity == "exit" or quantity == "stop":
                    return quantity
                confirm = await self.trade_buy_step_4_confirm(command, discord_id, character_name, item_name, quantity)
                if confirm == "exit" or confirm == "stop":
                    return confirm
            elif trade_type == "Sell":
                item_name = await self.trade_sell_step_1_item(command, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                quantity = await self.trade_sell_step_2_quantity(command, character_name, item_name)
                if quantity == "exit" or quantity == "stop":
                    return quantity
                price = await self.trade_sell_step_3_price(command, item_name)
                if price == "exit" or price == "stop":
                    return price
                confirm = await self.trade_sell_step_4_confirm(command, discord_id, character_name,
                                                               item_name, quantity, price)
                if confirm == "exit" or confirm == "stop":
                    return confirm
                return
            elif trade_type == "Stop trading":
                item_name = await self.trade_stop_step_1_item(command, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                confirm = await self.trade_stop_step_2_confirm(command, discord_id, character_name, item_name)
                if confirm == "exit" or confirm == "stop":
                    return confirm
                return

    async def trade_step_1_choice(self, command, character_name):
        # collect information about how much crafting can be done
        option_list = Scripts.character_trade_options(character_name)
        option_question = "what would you like to do?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_buy_step_1_item_type_choice(self, command, gold, character_name):
        option_list = SQL_Lookup.trade_goods_types(character_name, gold)
        option_question = "What type of item are you trying to buy?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_buy_step_2_item_choice(self, command, gold, item_type, character_name):
        option_list = SQL_Lookup.trade_goods_items_by_type(character_name, gold, item_type)
        option_question = "which item are you trying to buy?"
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(":")
        return choice_details[0]

    async def trade_buy_step_3_quantity(self, command, character_name, item_name):
        character_gold = SQL_Lookup.character_gold_total(character_name)
        trade_good = SQL_Lookup.trade_item_details(character_name, item_name)
        maximum = min([trade_good.Quantity, int(character_gold/trade_good.Price)])
        if maximum == 1:
            choice = 1
        else:
            choice_question = "There are {} {} for sale, they cost {}g each and you have {}g. " \
                              "How many would you like to buy?"\
                .format(trade_good.Quantity, trade_good.Item, trade_good.Price, character_gold)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def trade_buy_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        trade_good = SQL_Lookup.trade_item_details(character_name, item_name)
        total_value = trade_good.Price * quantity
        question = "Do you want to buy {} {} for {}g each for a total of {}g?" \
            .format(quantity, item_name, trade_good.Price, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} Bought {} {} for {}g".format(character_name, quantity, trade_good, total_value)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_buy(character_name, item_name, quantity)

            target_discord = self.bot.get_user(SQL_Lookup.character_owner(trade_good.Character))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    async def trade_sell_step_1_item(self, command, character_name):
        option_list = SQL_Lookup.character_inventory(character_name)
        option_question = "What would you like to sell?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_sell_step_2_quantity(self, command, character_name, item_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "You own {} {}, how many would you like to put up for sale?".format(maximum, item_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def trade_sell_step_3_price(self, command, item_name):
        choice_question = "how much do you want to sell each {} for?".format(item_name)
        choice = await self.answer_with_float_number(command, choice_question, 100000000000)
        return choice

    async def trade_sell_step_4_confirm(self, command, discord_id, character_name,
                                        item_name, quantity: int, price: float):
        total_value = price * quantity
        question = "Do you want to put {} {} up for trade at {}g each for a total of {}g?" \
            .format(quantity, item_name, price, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} put {} {} up for trade at {}g".format(character_name, quantity, item_name, price)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_sell(character_name, item_name, quantity, price)

            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    async def trade_stop_step_1_item(self, command, character_name):
        option_list = SQL_Lookup.character_items_for_trade(character_name)
        option_question = "What would you like to stop selling?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_stop_step_2_confirm(self, command, discord_id, character_name, item_name):
        question = "Do you want stop selling {}?".format(item_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} stopped selling {}".format(character_name, item_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_stop(character_name, item_name)

            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    #  Work Menu
    async def work_menu(self, command, discord_id, character_name):
        welcome_message = "Work Menu: Type **STOP** at any time to go back to the player menu \n" \
                          "You can give up crafting for the week to work for another character"
        await command.message.author.send(welcome_message)
        while True:
            # get target name
            target_name = await self.work_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name
            # confirm the transaction
            confirm = await self.work_step_2_confirm(command, discord_id, character_name, target_name)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def work_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to pay"
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def work_step_2_confirm(self, command, discord_id, character_name, target_name):
        question = "Do you want work for {} this week?".format(target_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} worked for {}".format(character_name, target_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_stop(character_name, target_name)

            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Answers methods
    async def answer_from_list(self, command, question, option_list):
        options = Scripts.question_list(option_list)
        await command.message.author.send("{}\n{}".format(question, options))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"

            # check they picked an answer
            try:
                answer = int(msg.content)
                option = option_list[answer - 1]
                return option
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number from the "
                                                  "list of options".format(msg.content))
            except IndexError:
                await command.message.author.send("{} is not on the list, please enter a number from the "
                                                  "list of options".format(msg.content))

    async def answer_with_int_number(self, command, question, maximum):
        await command.message.author.send("{}".format(question))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"
            # check they picked an answer
            try:
                answer = int(msg.content)
                if answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("{} is too high, pick a number equal to or less than {}"
                                                      .format(answer, maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

    async def answer_with_float_number(self, command, question, maximum):
        await command.message.author.send("{}".format(question))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"
            # check they picked an answer
            try:
                answer = float(msg.content)
                if answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("{} is too high, pick a number under {}".format(answer, maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

    async def answer_with_statement(self, command):
        # check author
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
        except asyncio.TimeoutError:
            return "exit"
        # check the response
        if msg.content.lower() == "exit":
            reply = "exit"
        elif msg.content.lower() == "stop":
            reply = "stop"
        else:
            reply = msg.content.lower()
        return reply

    async def confirm(self, command):
        # check author
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
        except asyncio.TimeoutError:
            return "exit"
        # check the response
        if msg.content.lower() == "exit":
            reply = "exit"
        elif msg.content.lower() == "stop":
            reply = "stop"
        elif msg.content.lower() == "yes":
            reply = "Yes"
        else:
            reply = "No"
        return reply

    async def character_name_lookup(self, command, question, character_name):
        await command.message.author.send(question)

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            elif msg.content.lower() == "stop":
                return "stop"
            elif msg.content.lower() == character_name.lower():
                await command.message.author.send("You cannot give yourself an item")
            elif SQL_Check.character_exists(msg.content.lower()):
                return msg.content.lower()
            else:
                await command.message.author.send("{} is not a character, please "
                                                  "confirm the spelling and try again".format(msg.content.lower()))


def setup(bot):
    bot.add_cog(Player_Menu_Commands(bot))