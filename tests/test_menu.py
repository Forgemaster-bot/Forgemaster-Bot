import logging
import pytest
import mock
from collections import deque
import discord.ext.test as dpytest

# Our modules
import tests.test_data.test_menu_data as test_data
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

@pytest.mark.asyncio
async def test_help(player_message):
    await player_message('.help')
    dpytest.verify_message(test_data.help_msg)

@pytest.mark.asyncio
async def test_menu_not_as_player(nonplayer_message):
    await dpytest.empty_queue()
    await nonplayer_message('.menu')
    dpytest.verify_message(test_data.no_character_message)

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@pytest.mark.asyncio
async def test_menu_as_player(mock_wait_for_reply, player_message):
    replies =  deque(['exit'])
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)

    await dpytest.empty_queue()
    await player_message('.menu')
    dpytest.verify_embed(test_data.get_main_menu_embed('player'), allow_text=True, full=True)

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@pytest.mark.asyncio
async def test_character_sheet(mock_wait_for_reply, player_message):
    # Define expectations
    exp_embed = test_data.get_character_sheet_embed('player', level=True, free_profession=True)

    # Define mocks
    replies = deque(['1', 'exit'])
    num_replies = len(replies)
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)

    # Clear previous output
    await dpytest.empty_queue()

    # Run the test
    await player_message('.menu')

    # Remove messages for menus we don't care about
    for i in range(1, num_replies):
        dpytest.get_embed()

    # Assert expected outputs
    dpytest.verify_embed(exp_embed, allow_text=True, full=True)







