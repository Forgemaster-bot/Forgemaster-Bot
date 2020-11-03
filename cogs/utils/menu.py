from discord.ext import commands
import discord
import logging
import asyncio
import Exceptions
from Character.Character import Character
from cogs.utils import textmenus

log = logging.getLogger(__name__)

thumb_url = "https://cdn3.iconfinder.com/data/icons/fantasy-and-role-play-game-adventure-quest/" \
            "512/Helmet.jpg-512.png"

async def get_dm_channel(user):
    return user.dm_channel if user.dm_channel is not None else await user.create_dm()

async def get_channel(ctx, user=None, should_dm=True):
    return ctx.channel if not should_dm else await get_dm_channel(user or ctx.author)

async def start_menu(ctx, menu, should_dm=True, channel=None, should_raise_stop=False, author=None, **kwargs):
    m = menu(**kwargs, should_dm=should_dm)
    # channel = channel if channel else ctx.author.dm_channel
    channel = channel if channel else await get_channel(ctx, ctx.author, should_dm=should_dm)
    await m.start(ctx, wait=True, channel=channel, author=author)

    if m.exception and isinstance(m.exception, textmenus.StopException):
        log.debug("Stop exception received")
        if should_raise_stop:
            raise m.exception
    elif m.exception and isinstance(m.exception, textmenus.ExitException):
        log.debug("Exit exception received")
        raise m.exception
    elif m.exception and isinstance(m.exception, asyncio.TimeoutError):
        log.debug("Timeout exception received")
        raise m.exception
    elif not m.single_time:
        await start_menu(ctx, menu, should_dm=should_dm, channel=channel, should_raise_stop=should_raise_stop, **kwargs)
    return m


class BaseMenu(textmenus.Menu):
    """
    Helper base instance for textmenus.Menu. Reuses common code for finalize and getter for title
    """

    def __init__(self, title=None, embed_info=None, stop_on_first=True, **kwargs):
        # Handle creating embed info if one wasn't passed
        embed_info = embed_info if embed_info else self.create_embed_info()
        if 'should_dm' in kwargs:
            self.should_dm = kwargs.pop('should_dm')
        super().__init__(embed_info=embed_info, stop_on_first=True, **kwargs)
        self.single_time = stop_on_first
        self.timed_out = False
        try:
            self.title
        except AttributeError:
            self.title = title

    def get_title(self):
        try:
            return self.title
        except AttributeError:
            return None

    def finalize(self, timed_out):
        self.timed_out = timed_out

    def get_initial_message(self):
        return NotImplementedError

    def update_embed(self):
        return

    @staticmethod
    def create_embed_info() -> textmenus.EmbedInfo:
        colour = 0xd0021b
        thumbnail = thumb_url
        footer_text = None
        author = None
        fields = []
        return textmenus.EmbedInfo(thumbnail, author, colour, footer_text, fields)


class BaseCharacterMenu(BaseMenu):
    """
    Subclass of BaseMenu which requires a character to be passed at initialization.
    This allows us to pass this info to other submenus.
    """

    def __init__(self, character=None, **kwargs):
        super().__init__(**kwargs)
        self.character: Character = character
        self.update_embed()

def do_nothing(*args, **kwargs):
    pass

class ConfirmMenu(BaseMenu):
    """
    Menu for querying yes or no from user.
    """
    title = "Confirm Choice"

    def __init__(self, message=None, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.confirm = False

    def get_initial_message(self):
        return self.message

    async def on_confirm(self, payload):
        channel = await get_channel(self.ctx, user=payload.author, should_dm=self.should_dm)
        await channel.send("Confirming...")
        self.confirm = True

    async def on_reject(self, payload):
        channel = await get_channel(self.ctx, user=payload.author, should_dm=self.should_dm)
        await channel.send("Rejecting...")
        self.confirm = False

    @textmenus.submenu('Yes')
    async def confirm(self, payload):
        await self.on_confirm(payload)

    @textmenus.submenu('No')
    async def reject(self, payload):
        await self.on_reject(payload)

class ListMenu(BaseMenu):
    title = "List Menu"

    def get_initial_message(self):
        return self.message

    def __init__(self, title, message, choices, closure_func=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.closure_func = closure_func
        self.message = message
        self.choices = choices
        self.choice = None

        if isinstance(choices, dict):
            for key, value in self.choices.items():
                self.submenu(key)(self.make_choice_func(value) if closure_func is None else self.closure_func(value))
        elif isinstance(choices, list):
            for value in self.choices:
                self.submenu(value)(self.make_choice_func(value) if closure_func is None else self.closure_func(value))

    @staticmethod
    def make_choice_func(choice):
        async def choice_func(menu, payload):
            menu.choice = choice
        return choice_func

class ListCharacterMenu(BaseCharacterMenu, ListMenu):
    def __init__(self, character, next_menu, refresh=False, **kwargs):
        self.refresh = refresh
        self.next_menu = next_menu
        if refresh:
            self.character.refresh()
        super().__init__(character, **kwargs)


async def ask_for_quantity(ctx: commands.Context, max_num: int) -> int:
    async def wait_for_integer(message: discord.Message):
        try:
            if ctx.author.id != message.author.id or ctx.channel.id != message.channel.id:
                return False
            content = message.content.lower()
            if content == 'stop' or content == 'exit':
                return True
            value = int(message.content)
            if value < 0 or value > max_num:
                await message.author.send(f"Must be between 0 and {max_num}, 'stop', or 'exit. Please try again.")
                return False
            return True
        except ValueError:
            await message.author.send(f"Must be between 0 and {max_num}, 'stop', or 'exit. Please try again.")
            return False

    await ctx.channel.send(f"How many would you like to craft? You may craft up to {max_num}. "
                           f"[Please input an integer value between 0 and {max_num}, 'stop', or 'exit']")
    try:
        msg = await ctx.bot.wait_for('message', check=wait_for_integer, timeout=30)
        return int(msg.content)
    except asyncio.TimeoutError:
        await ctx.channel.send(f"Timed out, aborting...")
        raise Exceptions.StopException
    except ValueError:
        await ctx.channel.send(f"Invalid number, aborting...")
        raise Exceptions.StopException
