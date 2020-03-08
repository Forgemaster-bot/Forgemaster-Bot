from discord.ext import commands
import asyncio

import Command_Check
import Command_Execute
import Quick_Python
import Quick_SQL
import SQL_Lookup
import SQL_Check


class Crafting_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Craft', help="[Character] Craft items with your skills")
    async def craft(self, command):
        character_name = command.message.content.replace('$Craft ', '')
        discord_id = command.message.author.id
        command_check = Command_Check.craft(character_name, discord_id)
        if not command_check[0]:
            await command.send(command_check[1])
        else:
            crafting = True
            while crafting:
                # collect information about how much crafting can be done
                welcome_message = Command_Execute.crafting_message(character_name)
                gold_limit = Command_Execute.crafting_gold_limit(character_name)
                await command.message.author.send(welcome_message)
                # find crafting skills, choose if more than one
                if SQL_Check.character_has_multiple_profession(character_name):
                    profession_list = SQL_Lookup.character_skill_profession(character_name)
                    profession_question = "Please enter the number of the profession to use"
                    skill_choice = await self.answer_from_list(command, profession_question, profession_list)
                    if not skill_choice[0]:
                        break
                    skill = skill_choice[1]
                else:
                    skill = SQL_Lookup.character_skill_profession(character_name)[0]

                # find crafting types, choose if more than one
                profession_choices = SQL_Lookup.profession_choice(skill)
                if profession_choices > 1:
                    crafting_type_list = ("Craft a mundane item",
                                          "Craft a consumable from a recipe",
                                          "Experiment with ingredients")
                    craft_choice_question = "What would you like to craft?"
                    craft_type_choice = await self.answer_from_list(command, craft_choice_question, crafting_type_list)
                    if not craft_type_choice[0]:
                        crafting = False
                        break
                    craft_type = craft_type_choice[1]
                elif profession_choices == 1:
                    craft_type = "Craft a mundane item"
                else:
                    await command.author.send("{} has nothing to craft yet".format(skill))
                    break
                # crafting mundane items
                if craft_type == "Craft a mundane item":
                    # Pick type of item to make
                    item_type_list = SQL_Lookup.profession_item_type_list(skill, gold_limit)
                    if len(item_type_list) > 1:
                        item_type_question = "Please enter the number of the of item type would you like to craft"
                        item_type_choice = await self.answer_from_list(command, item_type_question, item_type_list)
                        if not item_type_choice[0]:
                            crafting = False
                            break
                        item_type = item_type_choice[1]
                    else:
                        item_type = item_type_list[0]
                    # Pick the item to craft
                    item_list = SQL_Lookup.profession_item_list(skill, item_type, gold_limit)
                    item_question = "Please enter the number of the item would you like to craft?"
                    item_choice = await self.answer_from_list(command, item_question, item_list)
                    if not item_choice[0]:
                        crafting = False
                        break
                    item = SQL_Lookup.item_detail(item_choice[1])

                    #  Quantity, if there making something under 100g then enter the quantity, otherwise its always 1
                    max_quantity = int(gold_limit / (item.Value/2))
                    if item.Value < 100 and max_quantity >= 2:
                        quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                                            "you can make up to {}. How many would you like to make?"\
                            .format(item.Value/2, item.Name, max_quantity)
                        quantity_choice = await self.answer_with_number(command, quantity_question, max_quantity)
                        if not quantity_choice[0]:
                            crafting = False
                            break
                        else:
                            quantity = quantity_choice[1]
                    else:
                        quantity = 1
                    await command.author.send("Do you want to craft {} {} for {}g? [yes/no]"
                                              .format(quantity, item.Name, (item.Value/2)*quantity))
                    reply = await self.craft_confirm(command)
                    if reply == "Yes":
                        await command.author.send("crafting..")
                        Quick_SQL.log_craft_command(character_name, item.Name, quantity,
                                                    (item.Value/2)*quantity, discord_id)
                        Command_Execute.craft_item(character_name, item.Name, quantity)
                        await command.author.send("You crafted {} {} for {}g".format(quantity, item.Name, item.Value/2))
                        crafting = False
                    else:
                        crafting = False
                elif craft_type == "Craft a consumable from a recipe":
                    await command.author.send("consumable crafting is still in development, come back later")
                    crafting = False
                elif craft_type == "Experiment with ingredients":
                    await command.author.send("experimenting is still in development, come back later")
                    crafting = False
            await command.author.send("Crafting Ended")

    @commands.command(name='Work', help="[Your Character],[Employers Character Name] work for someone this week.")
    async def working(self, command):
        trim_message = command.message.content.replace('$Work ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.work(trim_message, discord_id)
        await command.send(command_check[1])
        test = 1
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("selling")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.work(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Sale command stopped")
                    break

    async def answer_from_list(self, command, question, option_list):
        options = Quick_Python.question_list(option_list)
        await command.message.author.send("{}\n{}".format(question, options))
        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
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

    async def answer_with_number(self, command, question, maximum):
        await command.message.author.send("{}".format(question))
        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
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

    async def craft_confirm(self, command):
            # check author
            def check_reply(user_response):
                return user_response.author == command.author and user_response.channel.type[1] == 1
            # send the user the message
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
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
    bot.add_cog(Crafting_Commands(bot))
