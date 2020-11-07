import asyncio
import discord
from discord.ext import commands

import Quick_Python
import Connections
from Mod_Menu import Scripts
import Character.CharacterInfoFacade as CharacterInfoFacade
from Character.Character import Character


class Mod_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Character
    @commands.command(name='Create',
                      help="[Discord ID],[Character name],[Race],[Background],"
                           "[Class],[Str],[Dex],[Con],[Int],[Wis],[Cha],[Gold]",
                      aliases=['create']
                      )
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def create_character(self, command, *, args):
        trim_message = args
        command_check = Scripts.create_character_check(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.create_character_execute(trim_message)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Create character command stopped")
                    break

    @commands.command(name='Refresh', help='[Character]', aliases=['refresh'])
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def character_refresh(self, command, *, args):
        trim_message = args
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
    async def add_feat(self, command, *, arg):
        command_check = Scripts.add_feat_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.add_feat_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='RemoveFeat', help="[Character],[Feat or ASL]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def remove_feat(self, command, *, arg):
        command_check = Scripts.remove_feat_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.remove_feat_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='Item', help="use help for more information"
                                        "\n1) [Character Name], [Item:Quantity], [Item:Quantity]..."
                                        "\nExample - Cogs,Dagger:2, Pickaxe:3"
                                        "\n2) [Item Name], [Character Name:Quantity], [Character Name:Quantity]"
                                        "\nExample - Rations, Cogs:4,Ratagan:-2",
                      aliases=['item'])
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def item(self, command, *, arg):
        command_check = Scripts.item_check(arg)
        await command.send(command_check)
        while True:
            # Get confirmation from user
            reply = await self.confirm(command)
            if reply == "Yes":
                await command.send("Updating roster...")
                author = command.message.author
                log = Scripts.item_execute(arg, author)
                Connections.sql_log_command(command)
                await command.send(Quick_Python.list_to_table(log))
                await Connections.log_to_discord(self, Quick_Python.list_to_table(log))
                return
            else:
                await command.send("Give item command stopped")
                return

    # NPC
    @commands.command(name='NPC', help="[NPC Name]:[Dialog]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def npc_say(self, command, *, arg):
        await command.message.delete()
        response = Scripts.npc_talk_execute(arg)
        await command.send(response)

    # Skills
    @commands.command(name='AddSkill', help="[Character],[Skill], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def add_skill(self, command, *, arg):
        command_check = Scripts.skill_add_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.skill_add_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Give skill command stopped")
                    break

    @commands.command(name='RemoveSkill', help="[Character],[Skill], Optional : [Double]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def skill_remove(self, command, *, arg):
        command_check = Scripts.skill_remove_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.skill_remove_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Remove skill command stopped")
                    break

    # Stats
    @commands.command(name='ChangeStat', help="[Character],[Stat],[Amount]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def stat_change(self, command, *, arg):
        command_check = Scripts.stat_raise_check(arg)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    log = Scripts.stat_change_execute(arg)
                    Connections.sql_log_command(command)
                    await command.send(log)
                    break
                else:
                    await command.send("Give feat command stopped")
                    break

    @commands.command(name='SyncPlayers', help='updates database with all user Id and names')
    @commands.has_any_role('DMs', 'Mods', 'Forge Smiths')
    async def sync_players(self, command):
        response = await Scripts.sync_players_execute(command)
        await command.send(response)

    @commands.command(name='RollCheck', help='[Discord Name]')
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def roll_check(self, command, *, arg):
        if arg == "":
            await command.send("You must pass the discord id of player you'd like to check.")
            return
        command_check = Scripts.roll_check_check(arg)
        if command_check[0]:
            response = Scripts.roll_check_execute(arg)
            await command.send(response)
        else:
            await command.send(command_check[1])

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

    @commands.command(name='character', help="Prints character info for character name passed. Args: [Character Name]")
    #@commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def character_id(self, ctx, *, arg):
        info_list = CharacterInfoFacade.interface.fetch_by_character_name(arg)
        for info in info_list:
            character = Character(info.character_id)
            embed = discord.Embed(title=f"{character.info.name}'s Info")
            # embed.add_field(name="character_name", value="{character_name}", inline=True)
            # embed.add_field(name="name", value="value", inline=True)
            for item in character.get_formatted_character_info_list():
                embed.add_field(name='\u200b', value=f"{item}", inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mod_Commands(bot))
