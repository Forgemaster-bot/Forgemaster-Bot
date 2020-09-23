import discord
import functools
import logging
import pytest
import mock
import difflib
import pprint
from collections import deque
import discord.ext.test as dpytest
from discord.ext.test import backend, get_config, message

# Our modules
import tests.test_data.test_menu_data as test_data
import bot as testbot
from cogs.Menu import Menu

"""
Setup detailed debugging log 'levels'
"""
log_messages = True
log_embeds = True

"""
Setup logger
"""
log = logging.getLogger(__name__)

"""
Setup test globals
"""
cog = None
player: discord.User = None
player_message = None
non_player: discord.User = None
non_player_message = None


def set_player():
    global player, player_message
    player = backend.make_member(
            backend.make_user(**test_data.discord_info_lookup['player']),
            get_config().guilds[0]
        )
    player_message = functools.partial(message, member=player)

def set_non_player():
    global non_player, non_player_message
    non_player = backend.make_member(
            backend.make_user(**test_data.discord_info_lookup['non_player']),
            get_config().guilds[0]
        )
    non_player_message = functools.partial(message, member=non_player)


def setup_function():
    log.debug(f"Setting up {__name__} ...")
    global cog
    # Override initial extensions and limit to just tested cog
    testbot.TestBot.initial_extensions = []
    # Create bot and pass to dpytest for stubbing/test cases
    bot = testbot.TestBot()
    cog = Menu(bot)
    bot.add_cog(cog)
    dpytest.configure(bot)
    set_player()
    set_non_player()
    test_data.create_characters()


def compare_message(left_msg, right_msg):
    log.debug(list(difflib.Differ().compare(left_msg, right_msg)))

def compare_dicts(d1, d2):
    return ('\n' + '\n'.join(difflib.ndiff(
                   pprint.pformat(d1).splitlines(),
                   pprint.pformat(d2).splitlines())))


def verify_message(msg: str):
    if msg is not None:
        dpytest.verify_message(msg)


def verify_embed(embed: discord.Embed):
    if embed is not None:
        peek = dpytest.get_embed(peek=True)
        assert peek.to_dict() == embed.to_dict()

def wait_until_menu(title: str):
    import time
    time.sleep(4)

class MockPayload:
    def __init__(self, content: str):
        self.content: str = content

def make_side_effect_wait_for_reply(replies: deque):
    async def mock_wait_for_reply(*args, **kwargs) -> MockPayload:
        if len(replies):
            return MockPayload(replies.popleft())
        return MockPayload('exit')
    return mock_wait_for_reply

@pytest.mark.asyncio
async def test_help():
    await player_message('.help')
    dpytest.verify_message(test_data.help_msg)

@pytest.mark.asyncio
async def test_menu_not_as_player():
    await dpytest.empty_queue()
    await non_player_message('.menu')
    dpytest.verify_message(test_data.no_character_message)

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@pytest.mark.asyncio
async def test_menu_as_player(mock_wait_for_reply):
    replies =  deque(['exit'])
    mock_wait_for_reply.side_effect = make_side_effect_wait_for_reply(replies)

    await dpytest.empty_queue()
    await player_message('.menu')
    dpytest.verify_embed(test_data.get_main_menu_embed('player'), allow_text=True)

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@pytest.mark.asyncio
async def test_character_sheet(mock_wait_for_reply):
    # Define expectations
    exp_embed = test_data.get_character_sheet_embed('player', level=True)

    # Define mocks
    replies = deque(['1', 'exit'])
    num_replies = len(replies)
    mock_wait_for_reply.side_effect = make_side_effect_wait_for_reply(replies)

    # Clear previous output
    await dpytest.empty_queue()

    # Run the test
    await player_message('.menu')

    # Remove messages for menus we don't care about
    for i in range(1, num_replies):
        dpytest.get_embed()
        # log.debug(f"{i}: {repr(dpytest.get_embed().to_dict())}")

    # Assert expected outputs
    dpytest.verify_embed(exp_embed, allow_text=True)
    # embed = dpytest.get_embed()
    # log.debug(compare_dicts(exp_embed.to_dict(), embed.to_dict()))
    # assert dpytest.embed_eq(embed, exp_embed)






