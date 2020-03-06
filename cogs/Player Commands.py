from discord.ext import commands
import asyncio

import Command_Check
import Quick_SQL
import Command_Execute


class Player_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Level up
    @commands.command(name='LevelUp', help="[Character Name],[Class]")
    async def level_up(self, command):
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

    # Roll Stats
    @commands.command(name='randchar', help='[Dice Number] + D + [Number of sides] example 4D6')
    async def dice_roll(self, command):
        Quick_SQL.log_command(command)
        discord_id = str(command.message.author.id)
        discord_name = str(command.message.author.display_name)

        command_check = Command_Check.roll_stats(discord_id, discord_name)
        if command_check[0]:
            response = Command_Execute.rand_char(discord_id)
            await command.send(response)
        else:
            await command.send(command_check[1])

    # Shop
    '''
    @commands.command(name='ShopBuy', help="[Character]],[Item],[Quantity]")
    async def shop_buy(self, command):
        trim_message = command.message.content.replace('$ShopBuy ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.shop_buy(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("buying...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.shop_buy(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("For sale command stopped")
                    break

    @commands.command(name='Sell', help="[Character]],[Item],[Quantity]")
    async def shop_sell(self, command):
        trim_message = command.message.content.replace('$ShopSell ', '')
        discord_id = str(command.message.author.id)
        command_check = Command_Check.shop_sell(trim_message, discord_id)
        await command.send(command_check[1])
        if command_check[0]:
            while True:
                # Get confirmation from user
                reply = await self.confirm(command)
                if reply == "Yes":
                    await command.send("selling...")
                    Quick_SQL.log_command(command)
                    response = Command_Execute.shop_buy(trim_message)
                    await command.send(response)
                    break
                else:
                    await command.send("For sale command stopped")
                    break
    '''
    # Trade
    @commands.command(name='TradeSell', help='[Character],[Item],[Price],[Quantity]')
    async def trade_sell(self, command):
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
