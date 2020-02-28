from discord.ext import commands
import asyncio

import Command_Check
import Quick_SQL
import Command_Execute


class Player_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Roll Stats
    @commands.command(name='randchar', help='[Dice Number] + D + [Number of sides] example 4D6')
    async def dice_roll(self, command):
        Quick_SQL.log_command(command)
        discord_id = str(command.message.author.id)
        command_check = Command_Check.roll_stats(discord_id)
        if command_check[0]:
            response = Command_Execute.rand_char(discord_id)
            await command.send(response)
        else:
            await command.send(command_check[1])

    # Level up
    @commands.command(name='LevelUp', help="[Character Name],[Class]")
    async def level_up(self, command):
            await command.send("working...")
            trim_message = command.message.content.replace('$LevelUp ', '')
            discord_id = str(command.message.author.id)
            command_check = Command_Check.level_up(trim_message, discord_id)
            await command.send(command_check[1])
            if command_check[0]:
                while True:
                    # Get confirmation from user
                    reply = await self.confirm(command)
                    if reply == "Yes":
                        await command.send("Adding level...")
                        Quick_SQL.log_command(command)
                        response = Command_Execute.level_up(trim_message)
                        await command.send(response)
                        break
                    else:
                        await command.send("level up command stopped")
                        break

    @commands.command(name='TradeSell', help='[Character],[Item],[Price],[Quantity]')
    async def trade_sell(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$TradeSell ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.trade_sell(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Putting items up for sale...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.trade_sell(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("For sale command stopped")
                    break

    @commands.command(name='TradeBuy', help="[Character],[Seller's Name],[Item],[Quantity]")
    async def trade_buy(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$TradeBuy ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.trade_buy(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("buying...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.trade_buy(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("For sale command stopped")
                    break

    @commands.command(name='TradeStop', help="[Character],[Item] Stop the sale of an item")
    async def trade_stop(self, command):
        await command.send("working...")
        trim_message = command.message.content.replace('$TradeStop ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.trade_stop(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("Stopping the sale...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.trade_stop(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("For sale command stopped")
                    break

    @commands.command(name='ListSkills', help="list available skills")
    async def list_skills(self, command):
        response = Command_Execute.info_skills()
        await command.send(response)

    @commands.command(name='ListClasses', help="list available classes")
    async def list_classes(self, command):
        response = Command_Execute.info_classes()
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
    bot.add_cog(Player_Commands(bot))
