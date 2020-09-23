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
import datetime

# Our modules
import tests.test_data.test_menu_data as test_data
import bot as testbot
from cogs import auction
from textwrap import dedent

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
player_message: functools.partial = None
admin: discord.User = None
admin_message: functools.partial = None


def set_player():
    global player, player_message
    player = backend.make_member(
            backend.make_user(**test_data.discord_info_lookup['player']),
            get_config().guilds[0]
        )
    player_message = functools.partial(message, member=player)

def set_admin():
    global admin, admin_message
    guild = get_config().guilds[0]
    admin = backend.make_member(
            backend.make_user(**test_data.discord_info_lookup['admin']),
            guild,
            roles=[backend.make_role("Admins", guild, permissions=8)]
        )
    admin_message = functools.partial(message, member=admin)

auction_lookup = {
    1, auction.AuctionTable.Row(item='1', auto_award=False, start=datetime.datetime(2020, 1, 1))
}


def setup_function():
    log.debug(f"Setting up {__name__} ...")
    global cog
    # Override initial extensions and limit to just tested cog
    testbot.TestBot.initial_extensions = []
    # Create bot and pass to dpytest for stubbing/test cases
    bot = testbot.TestBot()
    cog = auction.Auction(bot)
    bot.add_cog(cog)
    dpytest.configure(bot)
    set_player()
    set_admin()
    test_data.create_characters()

def make_auction_embed(title, description, fields=None):
    data = test_data.get_base_embed_dict(title, description, fields, color=0xFFEF00)
    if fields is None:
        data.pop('fields')
    return discord.Embed.from_dict(data)

def compare_message(left_msg, right_msg):
    log.debug(list(difflib.Differ().compare(left_msg, right_msg)))

def compare_dicts(d1, d2):
    return ('\n' + '\n'.join(difflib.ndiff(
                   pprint.pformat(d1).splitlines(),
                   pprint.pformat(d2).splitlines())))

def get_embed_and_compare(exp_embed: discord.Embed):
    actual_embed = dpytest.get_embed()
    log.debug(actual_embed.to_dict())
    log.debug(compare_dicts(exp_embed.to_dict(), actual_embed.to_dict()))


def verify_message(msg: str):
    if msg is not None:
        dpytest.verify_message(msg)


def verify_embed(embed: discord.Embed):
    if embed is not None:
        peek = dpytest.get_embed(peek=True)
        assert peek.to_dict() == embed.to_dict()

class MockPayload:
    def __init__(self, content: str):
        self.content: str = content

def make_side_effect_wait_for_reply(replies: deque):
    async def mock_wait_for_reply(*args, **kwargs) -> MockPayload:
        if len(replies):
            return MockPayload(replies.popleft())
        return MockPayload('exit')
    return mock_wait_for_reply

def make_side_effect_datetime_now(year, month, day, hour=0, minute=0, second=0, microsecond=0):
    def mocked_get_now(cls, tz=None):
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                 microsecond=microsecond)
    return mocked_get_now


@pytest.mark.asyncio
async def test_auction():
    await admin_message('.auction')
    exp_descrip = dedent("""\
        **bids** - Check bids for an auction
        **history** - Lists all past auctions
        **start** - Starts an auction.""")
    exp_embed = make_auction_embed('Auction Help', exp_descrip, None)
    dpytest.verify_embed(exp_embed, allow_text=True)

@pytest.mark.asyncio
async def test_auction_bad_permissions():
    with pytest.raises(discord.ext.commands.errors.CheckAnyFailure) as err:
        await player_message('.auction')

@pytest.mark.asyncio
async def test_auction_start(monkeypatch):
    # Define expected results
    item = "test123"
    title = f"Auction for {item}"
    description = 'A blind auction has started for an item! ' \
                  'If you wish to place a bid, simply react to this message with \N{WHITE HEAVY CHECK MARK}. ' \
                  'I will then message you directly with a request for your bid. ' \
                  'After <duration> has expired, the winner will be announced. '
    fields = [
        {'inline': True, 'name': 'Item For Auction:', 'value': f"{item}"},
        {'inline': True, 'name': 'Auction Duration:', 'value': "Manually Controlled"}
    ]
    exp_embed = make_auction_embed(title, description, fields)
    # Define side effects
    class mydatetime(datetime.datetime): pass
    setattr(mydatetime, 'now', classmethod(make_side_effect_datetime_now(2020, 1, 1)))
    monkeypatch.setattr(datetime, 'datetime', mydatetime)

    # Run test
    await dpytest.empty_queue()
    await admin_message(f".auction start {item}")
    # Assert results
    dpytest.verify_embed(exp_embed, allow_text=True)

#
# @pytest.mark.asyncio
# async def test_menu_not_as_player():
#     await dpytest.empty_queue()
#     await admin_message('.menu')
#     dpytest.verify_message(test_data.no_character_message)
#
# @mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
# @pytest.mark.asyncio
# async def test_menu_as_player(mock_wait_for_reply):
#     replies =  deque(['exit'])
#     mock_wait_for_reply.side_effect = make_side_effect_wait_for_reply(replies)
#
#     await dpytest.empty_queue()
#     await player_message('.menu')
#     dpytest.verify_embed(test_data.get_main_menu_embed('player'), allow_text=True)
#
# @mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
# @pytest.mark.asyncio
# async def test_character_sheet(mock_wait_for_reply):
#     # Define expectations
#     exp_embed = test_data.get_character_sheet_embed('player', level=True)
#
#     # Define mocks
#     replies = deque(['1', 'exit'])
#     num_replies = len(replies)
#     mock_wait_for_reply.side_effect = make_side_effect_wait_for_reply(replies)
#
#     # Clear previous output
#     await dpytest.empty_queue()
#
#     # Run the test
#     await player_message('.menu')
#
#     # Remove messages for menus we don't care about
#     for i in range(1, num_replies):
#         dpytest.get_embed()
#         # log.debug(f"{i}: {repr(dpytest.get_embed().to_dict())}")
#
#     # Assert expected outputs
#     dpytest.verify_embed(exp_embed, allow_text=True)
#     # embed = dpytest.get_embed()
#     # log.debug(compare_dicts(exp_embed.to_dict(), embed.to_dict()))
#     # assert dpytest.embed_eq(embed, exp_embed)






