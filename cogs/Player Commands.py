from discord.ext import commands
import asyncio

import Command_Check
import Command_Execute
import Quick_SQL
import Quick_Python
import SQL_Lookup


class Player_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # crafting
    @commands.command(name='Craft', help="Start Crafting")
    async def craft(self, command):
        discord_id = command.message.author.id
        while True:
            character_list = SQL_Lookup.character_list(discord_id)
            if len(character_list) > 1:
                character_choice_question = "Which character is this for?"
                character_choice_answer = await self.answer_from_list(command, character_choice_question,
                                                                      character_list)
                if not character_choice_answer[0]:
                    break
                character_name = character_choice_answer[1]
            else:
                character_name = character_list[0]
            command_check = Command_Check.craft(character_name, discord_id)
            if not command_check[0]:
                await command.send(command_check[1])
                break
            # collect information about how much crafting can be done
            welcome_message = Command_Execute.crafting_message(character_name)
            gold_limit = Command_Execute.crafting_gold_limit(character_name)
            profession_list = SQL_Lookup.character_skill_profession(character_name)
            if len(profession_list) == 0:
                await command.message.author.send("You dont own the tools for any of your professions")
                break
            await command.message.author.send(welcome_message)
            # check for skills and tools
            if len(profession_list) == 1:
                skill = profession_list[0]
            else:
                profession_question = "Please enter the number of the profession to use"
                skill_choice = await self.answer_from_list(command, profession_question, profession_list)
                if not skill_choice[0]:
                    break
                skill = skill_choice[1]
            # find crafting types, choose if more than one
            profession_choices = SQL_Lookup.profession_choice(skill)
            if len(profession_choices) == 1:
                craft_type = profession_choices[0]
            else:
                craft_choice_question = "What would you like to craft as a {}?".format(skill)
                craft_type_choice = await self.answer_from_list(command, craft_choice_question, profession_choices)
                if not craft_type_choice[0]:
                    break
                craft_type = craft_type_choice[1]
            # crafting mundane items
            if craft_type == "Mundane item":
                # Pick type of item to make
                item_type_list = SQL_Lookup.profession_item_type_list(skill, gold_limit)
                if len(item_type_list) == 0:
                    await command.message.author.send("You can afford to craft anything from this profession")
                    break
                if len(item_type_list) == 1:
                    item_type = item_type_list[0]
                else:
                    item_type_question = "With your {} tools you can make the following. Please enter the " \
                                         "number of the of item type would you like to craft".format(skill)
                    item_type_choice = await self.answer_from_list(command, item_type_question, item_type_list)
                    if not item_type_choice[0]:
                        break
                    item_type = item_type_choice[1]
                # Pick the item to craft
                item_list = SQL_Lookup.profession_item_list(skill, item_type, gold_limit)
                item_question = "Please enter the number of the item would you like to craft?"
                item_choice = await self.answer_from_list(command, item_question, item_list)
                if not item_choice[0]:
                    break
                item = SQL_Lookup.item_detail(item_choice[1])
                #  Quantity, if there making something under 100g then enter the quantity, otherwise its always 1
                max_quantity = int(gold_limit / (item.Value / 2))
                if item.Value < 100 and max_quantity >= 2:
                    quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                                        "you can make up to {}. How many would you like to make?" \
                        .format(item.Value / 2, item.Name, max_quantity)
                    quantity_choice = await self.answer_with_int_number(command, quantity_question, max_quantity)
                    if not quantity_choice[0]:
                        break
                    else:
                        quantity = quantity_choice[1]
                else:
                    quantity = 1
                await command.author.send("Do you want to craft {} {} for {}g? [yes/no]"
                                          .format(quantity, item.Name, (item.Value / 2) * quantity))
                reply = await self.private_confirm(command)
                if reply == "Yes":
                    await command.author.send("crafting..")
                    log = "{} made {} {} for {}g"\
                        .format(character_name, quantity, item.Name, (item.Value / 2) * quantity)
                    Quick_SQL.log_private_command(discord_id, log)
                    Command_Execute.craft_item(character_name, item.Name, quantity)
                    await command.author.send(
                        "You crafted {} {} for {}g".format(quantity, item.Name, (item.Value / 2) * quantity))
                break
            elif craft_type == "Craft a consumable from a recipe":
                await command.author.send("consumable crafting is still in development, come back later")
                break
            elif craft_type == "Experiment with ingredients":
                await command.author.send("experimenting is still in development, come back later")
                break
        await command.author.send("Crafting Ended")

    @commands.command(name='Work', help="[Character],[Employers Name] Work for someone this week.")
    async def working(self, command):
        trim_message = command.message.content.replace('$Work ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.work(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("getting to work..")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.work(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("work command stopped")
                    break

    # Give stuff
    @commands.command(name='Pay', help="[Character],[Target],[Amount],[Reason] Pay a character gold")
    async def pay(self, command):
        trim_message = command.message.content.replace('$Pay ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.pay(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("paying...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.pay(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Sale command stopped")
                    break

    # Level up
    @commands.command(name='LevelUp', help="[Character],[Class]")
    async def level_up(self, command):
        trim_message = command.message.content.replace('$LevelUp ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.level_up(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Adding level...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.level_up(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("level up command stopped")
                    break

    # Roll Stats
    @commands.command(name='randchar', help='Roll character stats')
    async def dice_roll(self, command):
        Quick_SQL.log_command(command)
        discord_id = str(command.message.author.id)
        discord_name = str(command.message.author.display_name)

        command_check = Command_Check.roll_stats(discord_id, discord_name)
        if command_check[0]:
            response = Command_Execute.rand_char(discord_id)
            await command.send(response)
        else:
            await command.send(command_check[1])

    @commands.command(name='Sell', help="[Character],[Item],[Quantity] Sell item to town at half value")
    async def shop_sell(self, command):
        trim_message = command.message.content.replace('$Sell ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.sell(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("selling...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.sell(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Sale command stopped")
                    break

    # Trade
    @commands.command(name='Trade', help='Start Trading')
    async def trade(self, command):
        discord_id = str(command.message.author.id)
        await command.message.author.send("Welcome to the trading window")
        while True:
            character_list = SQL_Lookup.character_list(discord_id)
            if len(character_list) > 1:
                character_choice_question = "Which character is this for?"
                character_choice_answer = await self.answer_from_list(command, character_choice_question,
                                                                      character_list)
                if not character_choice_answer[0]:
                    break
                character_name = character_choice_answer[1]
            else:
                character_name = character_list[0]
            trade_choice_question = "What would you like to do?"
            trade_choice_list = ["Buy", "Sell", "Stop Selling"]
            trade_choice_answer = await self.answer_from_list(command, trade_choice_question, trade_choice_list)
            if not trade_choice_answer[0]:
                break
            elif trade_choice_answer[1] == "Buy":
                gold_limit = SQL_Lookup.character_gold(character_name)
                # seller
                seller_list = SQL_Lookup.trade_sellers_list(character_name, gold_limit)
                seller_question = "who would you like to buy off?"
                seller_answer = await self.answer_from_list(command, seller_question, seller_list)
                if not seller_answer[0]:
                    break
                seller_name = seller_answer[1]

                # Item
                item_choice_question = "What would you like to buy off {}".format(seller_name)
                item_choice_list = SQL_Lookup.trade_seller_item_list(seller_name, gold_limit)
                item_choice_answer = await self.answer_from_list(command, item_choice_question, item_choice_list)
                if not item_choice_answer[0]:
                    break
                item_details = item_choice_answer[1].split(" - ")
                item_name = item_details[0]
                item_cost = float(item_details[1].replace("g", ""))

                # Quantity
                gold_quantity = int(gold_limit/item_cost)
                sale_quantity = SQL_Lookup.trade_item_quantity(seller_name, item_name)
                if gold_quantity < sale_quantity:
                    max_quantity = gold_quantity
                else:
                    max_quantity = sale_quantity
                if max_quantity > 2:
                    quantity_question = "You can buy up to {} {}, how many would you like to buy?".format(max_quantity,
                                                                                                          item_name)
                    quantity_answer = await self.answer_with_int_number(command, quantity_question, max_quantity)
                    if not quantity_answer[0]:
                        break
                    quantity = quantity_answer[1]
                else:
                    quantity = 1

                # confirm
                await command.author.send("Do you want to buy {} {} from {} at {}g? for a total of {} [yes/no]"
                                          .format(quantity, item_name, seller_name, item_cost, item_cost*quantity))
                reply = await self.private_confirm(command)
                if reply == "Yes":
                    await command.author.send("buying...")
                    log = "{} bought {} {} from{} at {}g for a total of {}".format(character_name, quantity, item_name,
                                                                                   seller_name, item_cost,
                                                                                   item_cost*quantity)
                    Quick_SQL.log_private_command(discord_id, log)
                    response = Command_Execute.trade_buy(character_name, seller_name, item_name, quantity)
                    await command.author.send(response)
                break
            elif trade_choice_answer[1] == "Sell":
                # Item
                item_choice_list = SQL_Lookup.character_inventory_sell_list(character_name)
                if len(item_choice_list) == 0:
                    await command.message.author.send("You dont have anything to sell")
                    break
                item_choice_question = "What would you like to sell?"
                item_choice_answer = await self.answer_from_list(command, item_choice_question, item_choice_list)
                if not item_choice_answer[0]:
                    break
                item_details = item_choice_answer[1].split(" (")
                item_name = item_details[0]
                # Price
                price_question = "how much do you want to sell each {} for?".format(item_name)
                price_answer = await self.answer_with_float_number(command, price_question, 100000000000)
                if not price_answer[0]:
                    break
                price = price_answer[1]

                # Quantity
                max_quantity = SQL_Lookup.character_item_quantity(character_name, item_name)
                if max_quantity >= 2:
                    quantity_question = "you have {} {}, how many do you want sell?".format(max_quantity, item_name)
                    quantity_answer = await self.answer_with_int_number(command, quantity_question, max_quantity)
                    if not quantity_answer[0]:
                        break
                    quantity = quantity_answer[1]
                else:
                    quantity = 1

                # confirm
                await command.author.send("Do you want to put {} {} up for sale at {}g? each [yes/no]"
                                          .format(quantity, item_name, price))
                reply = await self.private_confirm(command)
                if reply == "Yes":
                    await command.author.send("Selling...")
                    log = "{} put {} {} up for sale at {}g each".format(character_name, quantity, item_name, price)
                    Quick_SQL.log_private_command(discord_id, log)
                    response = Command_Execute.trade_sell(character_name, item_name, price, quantity)
                    await command.author.send(response)
                break
            elif trade_choice_answer[1] == "Stop Selling":
                # Item
                item_choice_list = SQL_Lookup.trade_seller_item_list(character_name, 1000000000)
                if len(item_choice_list) == 0:
                    await command.message.author.send("You arnt currently selling anything")
                    break
                item_choice_question = "What would you like to stop selling?"
                item_choice_answer = await self.answer_from_list(command, item_choice_question, item_choice_list)
                if not item_choice_answer[0]:
                    break
                item_details = item_choice_answer[1].split(" - ")
                item_name = item_details[0]
                # confirm
                await command.author.send("Do you want stop selling {}? [yes/no]".format(item_name))
                reply = await self.private_confirm(command)
                if reply == "Yes":
                    await command.author.send("stopping...")
                    log = "{] stopped selling {}".format(character_name, item_name)
                    Quick_SQL.log_private_command(discord_id, log)
                    response = Command_Execute.trade_stop(character_name, item_name)
                    await command.author.send(response)
                break
        await command.message.author.send("Trading closed")

    async def answer_from_list(self, command, question, option_list):
        options = Quick_Python.question_list(option_list)
        await command.message.author.send("{}\n{}".format(question, options))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return False, ""
            if msg.content.lower() == "stop":
                return False, ""

            # check they picked an answer
            try:
                answer = int(msg.content)
                option = option_list[answer - 1]
                return True, option
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
                return False, ""
            if msg.content.lower() == "stop":
                return False, ""
            # check they picked an answer
            try:
                answer = int(msg.content)
                if answer <= maximum:
                    return True, answer
                else:
                    await command.message.author.send("{} is too high, pick a number under {}".format(answer, maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number"
                                                  .format(msg.content))

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
                return False, ""
            if msg.content.lower() == "stop":
                return False, ""
            # check they picked an answer
            try:
                answer = float(msg.content)
                if answer <= maximum:
                    return True, answer
                else:
                    await command.message.author.send("{} is too high, pick a number under {}".format(answer, maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number"
                                                  .format(msg.content))

    async def private_confirm(self, command):
        # check author
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
        except asyncio.TimeoutError:
            return False, ""
        if msg.content.lower() == "stop":
            return False, ""
        # check content of response to see what the person wrote
        if msg.content.lower() == "yes":
            reply = "Yes"
        else:
            reply = "No"
        return reply

    async def confirm(self, command):
            # setup sub function to store new message
            def check_reply(m):
                return m.author == command.author
            # send the user the message
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
            except asyncio.TimeoutError:
                return "No"
            # check content of response to see what the person wrote
            if msg.content.lower() == "yes":
                reply = "Yes"
            else:
                reply = "No"
            return reply


def setup(bot):
    bot.add_cog(Player_Commands(bot))
