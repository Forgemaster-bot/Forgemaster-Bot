from discord.ext import commands
import asyncio
import Command_Execute


class Support_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Ping', help='Pong')
    async def ping(self, command):
        await command.send("Pong")

    @commands.command(name='SyncPlayers', help='updates database with all user Id and names')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def sync_players(self, command):
        await command.send("working...")
        response = Command_Execute.sync_players(command)
        await command.send(response)

    @commands.command(name='Test', help='Does stuff')
    @commands.check_any(commands.has_role('Bot-Support'))
    async def test(self, command):
        await command.send("ping")

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
