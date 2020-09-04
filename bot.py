from discord.ext import commands
import discord
import sys
import time
import traceback
import logging
import Connections

log = logging.getLogger(__name__)

initial_extensions = [
    'cogs.DM',
    'cogs.Utility',
    'cogs.Mod',
    'cogs.Player',
    'cogs.Admin'
]


class Forgemaster(commands.Bot):
    def __init__(self):
        super().__init__(**Connections.bot_config)
        for extension in initial_extensions:
            # noinspection PyBroadException
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_command_error(self, ctx, error):
        """
        Called on exception or error during a command.
        :param ctx: discord.Context object of the error
        :param error: Error information
        :return:
        """
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

        else:
            discord_id = ctx.author.id
            discord_command = ctx.message.clean_content
            Connections.sql_log_error(discord_id, discord_command, error.args[0])
            await ctx.send(error)

    async def on_ready(self):
        """
        Called when bot is starting up. Will set the message displayed.
        :return:
        """
        await self.wait_until_ready()
        game = discord.Game(Connections.bot_config['on_ready_message'])
        await self.change_presence(status=discord.Status.online, activity=game)
        await self.log_to_channel(f"Logged in at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    async def log_to_channel(self, msg):
        log_channel = self.get_channel(Connections.config["log-channel-id"])
        if log_channel is None:
            print(msg)
        else:
            await log_channel.send(msg)

    def run(self):
        super().run(Connections.config['token'], reconnect=True)
