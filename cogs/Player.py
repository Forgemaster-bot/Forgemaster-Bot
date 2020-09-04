from discord.ext import commands
import asyncio

import Connections
from Patreon.PatreonStatus import PatreonStatus
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Check
from Player_Menu import Scripts
from Player_Menu.Character_Sheet_Menu import Menu as CS_Menu
from Player_Menu.Workshop_Menu import Menu as WS_Menu
from Player_Menu.Market_Menu import Menu as MP_Menu
from Exceptions import StopException, ExitException

def get_character_limit(command: commands.Context):
    character_limit = SQL_Lookup.total_characters_allowed(command.message.author.id)
    return character_limit + PatreonStatus.get(command)


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players_in_menu = {}

    # Menu
    @commands.command(name='Menu', help="Main Player Menu", aliases=['menu'])
    async def player_menu(self, command: commands.context.Context):
        player_opened_menu = False
        try:
            if command.message.author.id in self.players_in_menu:
                await command.message.author.send("You are already accessing the menu.")
                return
            else:
                player_opened_menu = True
                self.players_in_menu[command.message.author.id] = None

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
                try:
                    try:
                        character_id = SQL_Lookup.character_id_by_character_name(character_name)
                    except AttributeError as e:
                        error_message = "You do not have a character which can access the menu."\
                                        "You will need to roll your stats and talk with a Mod to create your character."\
                                        "The 'randchar' command will randomly roll your characters stats. " \
                                        "Once this is done, a Mod can use the 'Create' command to create your character."
                        await command.message.author.send(error_message)
                        break
                    menu_option = await self.main_menu_choice(command, character_id)
                    if menu_option == "View your character sheet":
                        while True:
                            try:
                                menu = await CS_Menu.main_menu(self, command, discord_id, character_id)
                            except StopException as err:
                                break
                            if menu == "exit":
                                menu_option = "exit"
                                break
                            if menu == "stop":
                                break
                    elif menu_option == "Go to the workshop":
                        while True:
                            try:
                                menu = await WS_Menu.main_menu(self, command, discord_id, character_id)
                            except StopException as err:
                                break
                    elif menu_option == "Go to the market":
                        while True:
                            menu = await MP_Menu.main_menu(self, command, discord_id, character_id)
                            if menu == "exit":
                                menu_option = "exit"
                                break
                            if menu == "stop":
                                break
                    if menu_option == "exit":
                        break
                except ExitException as err:
                    menu_option = "exit"
                    if err.message is not None:
                        await command.message.author.send(err.message)

        finally:
            if player_opened_menu:
                self.players_in_menu.pop(command.message.author.id)
                await command.message.author.send("Menu closed")

    # Roll StatsPatreonStatus
    @commands.command(name='randchar', help='Roll character stats', aliases=['rollstats'])
    async def dice_roll(self, command):
        discord_id = str(command.message.author.id)
        discord_name = str(command.message.author.display_name)
        if not SQL_Check.player_exists(discord_id):
            sync = Scripts.sync_player(discord_id, discord_name)
            if not sync[0]:
                await command.send(sync)
        character_limit = get_character_limit(command)
        characters_total = SQL_Lookup.character_total(discord_id)
        roll_total = SQL_Lookup.character_roll_total(discord_id)
        if characters_total < character_limit:
            if roll_total < character_limit:
                Connections.sql_log_command(command)
                response = Scripts.rand_char(discord_id)
                await command.send(response)
            else:
                response = "You have already hit your max number of rolls. " \
                           "A mod can verify your rolls using the 'RollCheck' command."
                await command.send(response)

        else:
            rolls = SQL_Lookup.player_stat_roll(discord_id)
            info = "Current maximum number of characters reached [{}/{}].".format(characters_total, character_limit)
            await command.send(info)
            if not rolls:
                response = "Error: Player has no rolls stored. But, player has " \
                           "{}/{} characters.".format(characters_total, character_limit)
                await command.send(response)
                return
            for roll in rolls:
                previous_rolls = [roll.Roll_1, roll.Roll_2, roll.Roll_3,
                                  roll.Roll_4, roll.Roll_5, roll.Roll_6]
                if roll.Character_Name is None:
                    character_name = "Not used"
                else:
                    character_name = "Used for {}".format(roll.Character_Name)
                response = Scripts.stitch_list_into_string(previous_rolls)
                response = "Array: {}. {}".format(response, character_name)
                await command.send(response)

    # Menu commands
    async def character_choice(self, command, discord_id):
        option_list = SQL_Lookup.player_character_list(discord_id)
        if len(option_list) == 0:
            await command.message.author.send("You dont have any characters yet.")
            choice = "stop"
        elif len(option_list) == 1:
            choice = option_list[0]
        else:
            option_question = "Which character would you like to view the menu for?"
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def main_menu_choice(self, command, character_id):
        character_name = SQL_Lookup.character_name_by_character_id(character_id)
        option_list = Scripts.main_menu()
        if len(option_list) == 0:
            await command.message.author.send("{} doesnt have any options available".format(character_name))
            choice = "stop"
        else:
            option_question = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                              "Main Menu: Welcome {}, What would you like to do? Type **EXIT** to close the menu.\n" \
                              "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n" \
                .format(character_name)
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    # Answers methods
    async def answer_from_list(self, command, question, option_list):
        options = Scripts.question_list(option_list)
        maximum = len(option_list)
        if maximum == 0:
            await command.message.author.send("No options available")
            return "stop"
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
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                else:
                    # option = option_list[answer - 1].replace("'", "''")
                    return option_list[answer - 1]
            except IndexError:
                await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

    async def answer_from_list_craft(self, command, question, option_list):
        options = Scripts.question_list(option_list)
        maximum = len(option_list)
        if maximum == 0:
            await command.message.author.send("No options available")
            return "stop"
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
            if msg.content.lower() == "craft":
                return "craft"
            if msg.content.lower() == "stop":
                return "stop"

            # check they picked an answer

            try:
                answer = int(msg.content)
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                else:
                    option = option_list[answer - 1]
                    return option
            except IndexError:
                await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

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
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                elif answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, Please enter a number between 1 and {}"
                                                  .format(msg.content, maximum))

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
                if answer < 0:
                    await command.message.author.send("Please enter a number greater than 0".format(maximum))
                elif answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("Please enter a number greater than 0".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, Please enter a number greater than 0"
                                                  .format(msg.content))

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

    async def character_name_lookup(self, command, question, character_id):
        await command.message.author.send(question)

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            character_name = SQL_Lookup.character_name_by_character_id(character_id)
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
    bot.add_cog(PlayerCog(bot))
