from discord.ext import commands
import asyncio
import Connections
import Character.CharacterInfoFacade as CharacterInfoFacade
import Update_Google_Roster as Roster
from Character.Character import Character
from DM_Menu import Scripts
from DM_Menu import SQL_Lookup


class DMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='CharacterKill', help="[Character Name],[Reason]", aliases=['KillCharacter'])
    @commands.check_any(commands.has_role('Admins'), commands.has_role('DMs'))
    async def kill_character(self, command, *, arg):
        command_check = Scripts.kill_character_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.kill_character_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Kill character command stopped")
                    break

    # Gold
    @commands.command(name='AddGold', help="[Gold amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Admins'), commands.has_role('DMs'))
    async def change_gold(self, command, *, arg):
        command_check = Scripts.add_gold_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_gold_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Give gold command stopped")
                    break

    # XP
    @commands.command(name='AddXP', help="[XP amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Admins'), commands.has_role('DMs'))
    async def add_xp(self, command, *, arg):
        command_check = Scripts.add_xp_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_xp_execute(arg)
                    Connections.sql_log_command(command)
                    await Connections.log_to_discord(self, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Reward XP command stopped")
                    break

    # Add logxp
    @commands.command(name='LogXP', help="[Character]")
    @commands.check_any(commands.has_role('Admins'), commands.has_role('DMs'))
    async def log_xp(self, command, *, arg):
        command_check = Scripts.log_xp_check(arg)
        if command_check[0]:
            author = command.message.author
            log = Scripts.log_xp_execute(arg, author)
            Connections.sql_log_command(command)
            await command.send(log)
            await Connections.log_to_discord(self, log)
            Connections.sql_log_command(command)
            character_id = SQL_Lookup.character_id_by_character_name(arg)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(character_id))
            await target_discord.send(log)
        else:
            await command.send(command_check[1])

    @commands.command(name='RefreshRoster', help="Refreshes all character data in roster", aliases=['refreshroster'])
    @commands.check_any(commands.has_role('Admins'), commands.has_role('DMs'))
    async def refresh_roster(self, ctx):
        id_list = CharacterInfoFacade.interface.fetch_keys()
        await ctx.send("Updating roster...")
        for character_id in id_list:
            character = Character(character_id)
            Roster.update_character_in_roster(character)
        await ctx.send("Done!")

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
    bot.add_cog(DMCog(bot))
