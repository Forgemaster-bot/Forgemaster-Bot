from discord.ext import commands
import asyncio

import Command_Check
import Quick_SQL
import Command_Execute


class Mod_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Character
    @commands.command(name='CharacterCreate', help="[Discord ID],[Character name],[Race],[Background],[Class],"
                                                   "[Str],[Dex],[Con],[Int],[Wis],[Cha],[Gold]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def create_character(self, command):
        trim_message = command.message.content.replace('$CharacterCreate ', '')
        command_check = Command_Check.create_character(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.create_character(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Create character command stopped")
                    break

    #@commands.command(name='CharacterSync', help='[Character Name] - update the database from google sheets')
    #@commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    #async def sync_characters(self, command):
    #    trim_message = command.message.content.replace('$CharacterSync ', '')
    #    command_check = Command_Check.sync_character(trim_message)
    #    await command.send(command_check[1])
    #    if command_check[0]:
    #        while True:
    #            # Get confirmation from user
    #            reply = await self.confirm(command)
    #            if reply == "Yes":
    #                await command.send("Updating...")
    #                Quick_SQL.log_command(command)
    #                Command_Execute.character_sync(trim_message)
    #                await command.send("{} saved to SQL".format(trim_message))
    #                break
    #            else:
    #                await command.send("Sync Character command stopped")
    #                break

    @commands.command(name='CharacterRefresh', help='[Character Name]')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def character_refresh(self, command):
        trim_message = command.message.content.replace('$CharacterRefresh ', '')
        command_check = Command_Check.character_refresh(trim_message)
        if command_check[0]:
            await command.send("working...")
            Command_Execute.character_refresh(trim_message)
            await command.send("{} refreshed".format(trim_message))

    # Feats
    @commands.command(name='FeatAdd', help="[Character Name],[Feat or ASL]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def add_feat(self, command):
        trim_message = command.message.content.replace('$FeatAdd ', '')
        command_check = Command_Check.add_feat(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.add_feat(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='FeatRemove', help="[Character Name],[Feat or ASL]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def remove_feat(self, command):
        trim_message = command.message.content.replace('$FeatRemove ', '')
        command_check = Command_Check.remove_feat(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.remove_feat(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    # Skills
    @commands.command(name='SkillAdd', help="[Character Name],[Skill Name], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def add_skill(self, command):
        trim_message = command.message.content.replace('$SkillAdd ', '')
        command_check = Command_Check.skill_remove(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.skill_add(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give skill command stopped")
                    break

    @commands.command(name='SkillRemove', help="[Character Name],[Skill Name], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def skill_remove(self, command):
        trim_message = command.message.content.replace('$SkillRemove ', '')
        command_check = Command_Check.skill_remove(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.skill_remove(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Remove skill command stopped")
                    break

    # Stats
    @commands.command(name='StatChange', help="[Character Name],[Stat],[Amount]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def stat_change(self, command):
        trim_message = command.message.content.replace('$StatChange ', '')
        command_check = Command_Check.stat_raise(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.stat_change(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='RollCheck', help='[Character Name]')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def roll_check(self, command):
        trim_message = command.message.content.replace('$RollCheck ', '')
        command_check = Command_Check.roll_check(trim_message)
        if command_check[0]:
            response = Command_Execute.roll_check(trim_message)
            await command.send(response)

    async def confirm(self, command):
            # setup sub function to store new message
            def check_reply(m):
                return m.author == command.author

            # send the user the message
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check_reply)
            except asyncio.TimeoutError:
                return "No"
            # check content of response to see what the person wrote
            if msg.content.lower() == "yes":
                reply = "Yes"
            else:
                reply = "No"

            return reply


def setup(bot):
    bot.add_cog(Mod_Commands(bot))
