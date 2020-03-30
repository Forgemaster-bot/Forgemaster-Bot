from discord.ext import commands
import asyncio

from Mod_Menu import Scripts
import Connections


class Mod_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Character
    @commands.command(name='CharacterCreate', help="[Discord ID],[Character name],[Race],[Background],[Class],"
                                                   "[Str],[Dex],[Con],[Int],[Wis],[Cha],[Gold]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def create_character(self, command):
        trim_message = command.message.content.replace('$CharacterCreate ', '')
        command_check = Scripts.create_character_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.create_character_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Create character command stopped")
                    break

    @commands.command(name='CharacterRefresh', help='[Character]')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def character_refresh(self, command):
        trim_message = command.message.content.replace('$CharacterRefresh ', '')
        command_check = Scripts.character_refresh_check(trim_message)
        if command_check[0]:
            await command.send("working...")
            Scripts.character_refresh_execute(trim_message)
            await command.send("{} refreshed".format(trim_message))
        else:
            await command.send(command_check[1])

    # Feats
    @commands.command(name='AddFeat', help="[Character],[Feat or ASL]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def add_feat(self, command):
        trim_message = command.message.content.replace('$AddFeat ', '')
        command_check = Scripts.add_feat_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_feat_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='RemoveFeat', help="[Character],[Feat or ASL]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def remove_feat(self, command):
        trim_message = command.message.content.replace('$RemoveFeat ', '')
        command_check = Scripts.remove_feat_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.remove_feat_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    # NPC
    @commands.command(name='NPC', help="[NPC Name]:[Dialog]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def stat_change(self, command):
        await command.message.delete()
        trim_message = command.message.content.replace('$NPC ', '')
        response = Scripts.npc_talk_execute(trim_message)
        await command.send(response)

    # Skills
    @commands.command(name='AddSkill', help="[Character],[Skill], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def add_skill(self, command):
        trim_message = command.message.content.replace('$AddSkill ', '')
        command_check = Scripts.skill_add_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.skill_add_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Give skill command stopped")
                    break

    @commands.command(name='RemoveSkill', help="[Character],[Skill], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def skill_remove(self, command):
        trim_message = command.message.content.replace('$RemoveSkill ', '')
        command_check = Scripts.skill_remove_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.skill_remove_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Remove skill command stopped")
                    break

    # Stats
    @commands.command(name='ChangeStat', help="[Character],[Stat],[Amount]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def stat_change(self, command):
        trim_message = command.message.content.replace('$ChangeStat ', '')
        command_check = Scripts.stat_raise_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.stat_change_execute(trim_message)
                    Connections.log_command(command, log)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='SyncPlayers', help='updates database with all user Id and names')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def sync_players(self, command):
        response = Scripts.character_sync_execute(command)
        await command.send(response)

    @commands.command(name='RollCheck', help='[Discord Name]')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def roll_check(self, command):
        trim_message = command.message.content.replace('$RollCheck ', '')
        command_check = Scripts.roll_check_check(trim_message)
        if command_check[0]:
            response = Scripts.roll_check_execute(trim_message)
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
