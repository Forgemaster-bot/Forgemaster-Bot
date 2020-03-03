from discord.ext import commands
import asyncio

import SQL_Lookup
import SQL_Check
import Command_Check
import Quick_Python


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
                if SQL_Check.character_has_multiple_profession(character_name):
                    craft_skill = await self.pick_craft_skill(command, character_name)
                    crafting = craft_skill[0]
                else:
                    craft_skill = SQL_Lookup.character_skill_profession(character_name)

            await command.author.send("Crafting Ended")

    async def pick_craft_skill(self, command, character_name):
        profession = Quick_Python.stitch_table(SQL_Lookup.character_skill_profession(character_name))
        question = "Please choose a profession to use:\n{}".format(profession)
        await command.message.author.send(question)

        # setup sub function to do checks the returned message is from the user in private messages
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # run the check until 60 seconds has elapsed
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
        except asyncio.TimeoutError:
            return False, ""
        if msg.content == "EXIT":
            return False, ""

        # check content of response to see what the person wrote
        return True, msg.content.lower()


def setup(bot):
    bot.add_cog(Crafting_Commands(bot))