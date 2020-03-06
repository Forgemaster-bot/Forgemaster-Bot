from discord.ext import commands
import asyncio

import Command_Check
import Command_Execute
import Quick_Python
import SQL_Lookup
import SQL_Check


class Crafting_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Craft', help="[Character]")
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
                    profession_question = "Please choose a profession to use"
                    skill_choice = await self.answer_from_list(command, profession_question, profession_list)
                    if not skill_choice[0]:
                        break
                    skill = skill_choice[1]
                else:
                    skill = SQL_Lookup.character_skill_profession(character_name)[0]

                # find crafting types, choose if more than one
                if SQL_Check.profession_has_multiple_choice(skill):
                    crafting_type_list = ("Craft a mundane item",
                                          "Craft a consumable from a recipe",
                                          "Experiment with ingredients")
                    craft_choice_question = "What would you like to craft?"
                    craft_type_choice = await self.answer_from_list(command, craft_choice_question, crafting_type_list)
                    if not craft_type_choice[0]:
                        break
                    craft_type = craft_type_choice[1]
                else:
                    craft_type = "Craft a mundane item"

                # crafting mundane items
                if craft_type == "Craft a mundane item":
                    # Pick type of item to make
                    item_type_list = SQL_Lookup.profession_item_type_list(skill, gold_limit)
                    if len(item_type_list) > 1:
                        item_type_question = "what type of item would you like to craft?"
                        item_type_choice = await self.answer_from_list(command, item_type_question, item_type_list)
                        if not item_type_choice[0]:
                            break
                        item_type = item_type_choice[1]
                    else:
                        item_type = item_type_list[0]
                    # Pick the item to craft
                    item_list = SQL_Lookup.profession_item_list(skill, item_type, gold_limit)
                    item_question = "Which item would you like to craft?"
                    item_choice = await self.answer_from_list(command, item_question, item_list)
                    if not item_choice[0]:
                        break
                    item = SQL_Lookup.item_detail(item_choice[1])

                    #  Quantity, if there making something under 100g then enter the quantity, otherwise its always 1
                    max_quantity = int(gold_limit / item.Value)
                    if item.Value < 100 and max_quantity >= 2:
                        quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                                            "you can make up to {}. How many would you like to make?"\
                            .format(item.Value, item.Name, max_quantity)
                        quantity = await self.answer_with_number(command, quantity_question, max_quantity)

                    else:
                        quantity = 1
                    await command.author.send("You want to craft {} {} using the {} skill for {}g"
                                              .format(quantity, item.Name, skill, item.Value/2))
                    crafting = False
                elif craft_type == "Craft a consumable from a recipe":
                    crafting = False
                elif craft_type == "Experiment with ingredients":
                    crafting = False
            await command.author.send("Crafting Ended")

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
            if msg.content == "EXIT":
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
            if msg.content == "EXIT":
                return False, ""
            # check they picked an answer
            try:
                answer = int(msg.content)
                return True, answer
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number from the list of options"
                                                  .format(msg.content))


def setup(bot):
    bot.add_cog(Crafting_Commands(bot))
