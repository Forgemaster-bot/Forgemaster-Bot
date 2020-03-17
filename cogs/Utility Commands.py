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

    @commands.command(name='Test', help="message player test")
    async def test(self, command):
        target = 259051627145592832
        user = self.bot.get_user(target)
        await user.send("Test")
    # Yes/No response checker
    async def confirm(self, command):
        # setup sub function to store new message
        def check_reply(m):
            return m.author == command.author
        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=30.0, check=check_reply)
        except asyncio.TimeoutError:
            return "No"
        # check content of response to see what the person wrote
        if msg.content.lower() == "yes":
            reply = "Yes"
        else:
            reply = "No"
        return reply


def setup(bot):
    bot.add_cog(Support_Commands(bot))
