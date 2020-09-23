import pytest
import asyncio
import functools
import logging
import textwrap
import discord.ext.commands as commands
import discord.ext.test as dpytest

# Our modules
import bot as testbot
from cogs.Admin import Admin

log = logging.getLogger(__name__)
cog = None

def setup_function():
    log.debug(f"Setting up {__name__} ...")
    global cog
    # Override initial extensions and limit to just tested cog
    testbot.TestBot.initial_extensions = []
    # Create bot and pass to dpytest for stubbing/test cases
    bot = testbot.TestBot()
    bot.add_cog(Admin(bot))
    dpytest.configure(bot)

# import difflib
# d = difflib.Differ()
# log.debug(list(d.compare(msg.content,msg)))

@pytest.mark.asyncio
async def test_help():
    await dpytest.message('.help')
    msg = dpytest.get_message(peek=True)
    log.debug(msg.content)
    dpytest.verify_message(textwrap.dedent('''\
        ```
        This is a test bot for text menus.
        
        \u200bNo Category:
          help Shows this message
        
        Type .help command for more info on a command.
        You can also type .help category for more info on a category.
        ```'''))


