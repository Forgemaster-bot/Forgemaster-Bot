import discord
import logging
import pytest
import difflib
import pprint
from collections import deque
import discord.ext.test as dpytest
import datetime

# Our modules
import tests.test_data.test_menu_data as test_data
from cogs import auction
from textwrap import dedent
from tests import helper

pytestmark = pytest.mark.usefixtures("testbot")

"""
Setup detailed debugging log 'levels'
"""
log_messages = True
log_embeds = True

"""
Setup logger
"""
log = logging.getLogger(__name__)


auction_lookup = {
    1, auction.AuctionTable.Row(item='1', auto_award=False, start=datetime.datetime(2020, 1, 1))
}


def setup_function():
    log.debug(f"Setting up {__name__} ...")
    auction.AuctionTable.delete_all()
    auction.BidTable.delete_all()


def make_auction_embed(title, description, fields=None):
    data = test_data.get_base_embed_dict(title, description, fields, color=0xFFEF00)
    if fields is None:
        data.pop('fields')
    return discord.Embed.from_dict(data)


@pytest.mark.asyncio
async def test_auction(admin_message):
    await admin_message('.auction')
    exp_descrip = dedent("""\
        **bids** - Check bids for an auction
        **history** - Lists all past auctions
        **start** - Starts an auction.""")
    exp_embed = make_auction_embed('Auction Help', exp_descrip, None)
    dpytest.verify_embed(exp_embed, allow_text=True, full=True)


@pytest.mark.asyncio
async def test_auction_bad_permissions(player_message):
    with pytest.raises(discord.ext.commands.errors.CheckAnyFailure):
        await player_message('.auction')


@pytest.mark.asyncio
async def test_auction_start(monkeypatch, admin_message):
    # Define expected results
    item = "test123"
    time = "3 days"
    title = f"Auction for {item}"
    description = 'A blind auction has started for an item! ' \
                  'If you wish to place a bid, simply react to this message with \N{WHITE HEAVY CHECK MARK}. ' \
                  'I will then message you directly with a request for your bid. ' \
                  'After the duration has expired, the winner will be announced. '
    fields = [
        {'inline': True, 'name': 'Item For Auction:', 'value': f"{item}"},
        {'inline': True, 'name': 'Auction Duration:', 'value': f"{time}, 0:00:00"}
    ]
    exp_embed = make_auction_embed(title, description, fields)
    # Define side effects
    class MockDateTime(datetime.datetime): pass
    setattr(MockDateTime, 'now', classmethod(helper.make_side_effect_datetime_now(2020, 1, 1)))
    monkeypatch.setattr(datetime, 'datetime', MockDateTime)

    # Run test
    await dpytest.empty_queue()
    await admin_message(f".auction start {item} {time}")
    # Assert results
    dpytest.verify_embed(exp_embed, allow_text=True, full=True)

@pytest.mark.asyncio
async def test_help_nonplayer(nonplayer_message):
    await dpytest.empty_queue()
    await nonplayer_message('.help')
    msg = dpytest.get_message(peek=True)
    log.debug(msg.content)
    dpytest.verify_message(text='Admin', equals=False, contains=True)

@pytest.mark.asyncio
async def test_help_admin(admin_message):
    await dpytest.empty_queue()
    await admin_message('.help')
    msg = dpytest.get_message(peek=True)
    log.debug(msg.content)
    dpytest.verify_message(text='Admin', equals=False, contains=True)
