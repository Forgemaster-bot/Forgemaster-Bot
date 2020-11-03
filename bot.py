from discord.ext import commands
import discord
intents = discord.Intents.default()
intents.members = True

# from cogs.utils import context
import sys
import datetime
import traceback
import logging
import json
import config
from collections import deque

log = logging.getLogger(__name__)

class TestBot(commands.Bot):

    initial_extensions = [
        'cogs.Admin',
        'cogs.Menu',
        'cogs.auction',
        'cogs.Mod'
    ]

    def __init__(self):
        super().__init__(command_prefix=config.command_prefix,
                         description=config.description, intents=intents)

        """
        Set self attributes 
        """
        self.client_id = config.client_id
        self._prev_events = deque(maxlen=10)
        self.uptime = None
        """
        Load initial extensions
        """
        for extension in self.initial_extensions:
            # noinspection PyBroadException
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_socket_response(self, msg):
        self._prev_events.append(msg)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    async def on_ready(self):
        uptime = datetime.datetime.utcnow()
        if not hasattr(self, 'uptime') or self.uptime is None:
            self.uptime = uptime

        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def on_resumed(self):
        print('resumed...')

    async def process_commands(self, message):
        # ctx = await self.get_context(message, cls=context.Context)
        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        # try:
        if True:
            await self.invoke(ctx)
        # finally:
            # Just in case we have any outstanding DB connections
            # await ctx.release()

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def close(self):
        await super().close()

    def run(self):
        try:
            super().run(config.token, reconnect=True)
        finally:
            with open('prev_events.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, ensure_ascii=True, indent=4)
                    except:
                        fp.write(f'{data}\n')
                    else:
                        fp.write(f'{x}\n')

    @property
    def config(self):
        return __import__('config')
