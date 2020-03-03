from discord.ext import commands
import asyncio

import SQL_Lookup
import SQL_Check
import Command_Check


class Crafting_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Craft', help="[Character]")
    async def craft(self, command):
        trim_message = command.message.content.replace('$Craft ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.craft(trim_message, discord_id)
        if not command_check[0]:
            await command.send(command_check[1])
        while True:
            reply = await self.pick_craft_skill(command, 'I hear you want craft something is this true?')
            await command.author.send("you replied with {}".format(reply))
            break

    async def pick_craft_skill(self, command, question):
        await command.message.author.send(question)

        # setup sub function to do checks the returned message is from the user in private messages
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # run the check until 60 seconds has elapsed
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
        except asyncio.TimeoutError:
            return False, "No"

        # check content of response to see what the person wrote
        return msg.content.lower()


def setup(bot):
    bot.add_cog(Crafting_Commands(bot))