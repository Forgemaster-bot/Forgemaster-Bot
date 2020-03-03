from discord.ext import commands
import asyncio

import Command_Check
import Quick_Python
import SQL_Lookup
import SQL_Check
import SQL_Crafting_Lookup

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
                # If the player has multiple professions have them pick one to use
                if SQL_Check.character_has_multiple_profession(character_name):
                    crafting_choice = await self.pick_craft_skill(command, character_name)
                    if not crafting_choice[0]:
                        break
                    craft_skill = crafting_choice[1]
                else:
                    craft_skill = SQL_Crafting_Lookup.character_skill_profession(character_name)[0]

                await command.author.send("You picked {}".format(craft_skill))
                crafting = False
            await command.author.send("Crafting Ended")

    async def pick_craft_skill(self, command, character_name):
        while True:
            profession_list = SQL_Crafting_Lookup.character_skill_profession(character_name)
            profession_question = Quick_Python.stitch_table(profession_list)
            question = "Please choose a profession to use:\n{}".format(profession_question)
            await command.message.author.send(question)

            # setup sub function to do checks the returned message is from the user in private messages
            def check_reply(user_response):
                return user_response.author == command.author and user_response.channel.type[1] == 1

            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
            except asyncio.TimeoutError:
                return False, ""
            if msg.content == "EXIT":
                return False, ""

            # check they picked a skill
            crafting_skill = msg.content
            for prof in profession_list:
                if crafting_skill == prof:
                    return True, crafting_skill

def setup(bot):
    bot.add_cog(Crafting_Commands(bot))
