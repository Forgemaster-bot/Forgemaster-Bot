from discord.ext import commands
import asyncio

import Command_Check
import Command_Execute
import Quick_SQL


class DM_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='CharacterKill', help="[Character Name],[Reason]")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def kill_character(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$CharacterKill ', '')
        command_check = Command_Check.kill_character(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.kill_character(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Kill character command stopped")
                    break

    # Gold
    @commands.command(name='AddGold', help="[Gold amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def change_gold(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$AddGold ', '')
        command_check = Command_Check.add_gold(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.add_gold(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give gold command stopped")
                    break

    # NPC
    @commands.command(name='NPC', help="[NPC Name]:[Dialog]")
    @commands.check_any(commands.has_role('DMs'), commands.has_role('Mods'))
    async def stat_change(self, command):
        await command.message.delete()
        trim_message = command.message.content.replace('$NPC ', '')
        response = Command_Execute.npc_talk(trim_message)
        await command.send(response)

    @commands.command(name='ItemAdd', help="use help for more information"
                                           "\n1) [Character Name], [Item:Quantity], [Item:Quantity]..."
                                           "\nExample - Cogs,Dagger:2, Pickaxe:3, Leather:4"
                                           "\n2) [Item Name], [Character Name:Quantity], [Character Name:Quantity]"
                                           "\nExample - Rations, Cogs:4,Ratagan:2")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def add_item(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$ItemAdd ', '')
        command_check = Command_Check.add_item(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.add_item(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Give item command stopped")
                    break

    @commands.command(name='ItemRemove', help="[Character Name],[Item],[Quantity]")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def remove_item(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$ItemRemove ', '')
        command_check = Command_Check.remove_item(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    google_update = Command_Execute.remove_item(trim_message)
                    await command.send(google_update)
                    break
                else:
                    await command.send("Give item command stopped")
                    break

    # XP
    @commands.command(name='AddXP', help="[XP amount],[Character 1],[Character 2]...")
    @commands.check_any(commands.has_role('Head DM'), commands.has_role('DMs'))
    async def add_xp(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$AddXP ', '')
        command_check = Command_Check.reward_xp(trim_message)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Updating roster...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.add_xp(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("Reward XP command stopped")
                    break

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
