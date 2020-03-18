from discord.ext import commands
import asyncio
import Command_Execute


class Support_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ListSkills', help="list available skills")
    async def list_skills(self, command):
        response = Command_Execute.info_skills()
        await command.send(response)

    @commands.command(name='ListClasses', help="list available classes")
    async def list_classes(self, command):
        response = Command_Execute.info_classes()
        await command.send(response)

    @commands.command(name='Ping', help="Pong")
    async def ping(self, command):
        response = "Ping!"
        author = "<@{}>".format(command.message.author.id)
        await command.send("{} {}".format(author, response))


def setup(bot):
    bot.add_cog(Support_Commands(bot))
