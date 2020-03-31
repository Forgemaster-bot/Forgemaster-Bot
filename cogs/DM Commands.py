from discord.ext import commands
import asyncio

from DM_Menu import Scripts
from DM_Menu import SQL_Lookup
import Connections


class DM_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='CharacterKill', help="[Character Name],[Reason]")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def kill_character(self, command):
        trim_message = command.message.content.replace('$CharacterKill ', '')
        command_check = Scripts.kill_character_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.kill_character_execute(trim_message)
                    Connections.sql_log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Kill character command stopped")
                    break

    # Gold
    @commands.command(name='AddGold', help="[Gold amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def change_gold(self, command):
        trim_message = command.message.content.replace('$AddGold ', '')
        command_check = Scripts.add_gold_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_gold_execute(trim_message)
                    Connections.sql_log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Give gold command stopped")
                    break

    # XP
    @commands.command(name='AddXP', help="[XP amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def add_xp(self, command):
        trim_message = command.message.content.replace('$AddXP ', '')
        command_check = Scripts.add_xp_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_xp_execute(trim_message)
                    Connections.sql_log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Reward XP command stopped")
                    break

    # Add logxp
    @commands.command(name='LogXP', help="[Character]")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def log_xp(self, command):
        trim_message = command.message.content.replace('$LogXP ', '')
        command_check = Scripts.log_xp_check(trim_message)
        if command_check[0]:
            log = Scripts.log_xp_execute(trim_message)
            Connections.sql_log_command(command, log)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(trim_message))
            await Connections.log_to_discord(self, log)
            await target_discord.send(log)
        else:
            await command.send(command_check[1])

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
    bot.add_cog(DM_Commands(bot))
