from discord.ext import commands
from Utility_Menu import Scripts


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ListSkills', help="list available skills")
    async def list_skills(self, command):
        response = Scripts.info_skills()
        await command.send(response)

    @commands.command(name='ListClasses', help="list available classes")
    async def list_classes(self, command):
        response = Scripts.info_classes()
        await command.send(response)

    @commands.command(name='Ping', help="Pong")
    async def ping(self, command):
        response = "Ping!"
        author = "<@{}>".format(command.message.author.id)
        await command.send("{} {}".format(author, response))


def setup(bot):
    bot.add_cog(UtilityCog(bot))
