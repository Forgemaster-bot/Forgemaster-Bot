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

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@pytest.mark.asyncio
async def test_free_profession(mock_wait_for_reply, player_message):
    name = 'player'
    # Define expectations
    exp_embed = test_data.get_character_sheet_embed(name, level=True, free_profession=False, skills=['Weaver (D)'])

    # Define reply mocks to navigate menus:
    #   1 - Character Sheet
    #   2 - Select free profession menu
    #   10 - Select Weaver
    #   1 - Confirm the selection
    replies = deque(['1', '2', '10', '1', 'exit'])
    num_replies = len(replies)
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)

    # Clear previous output
    await dpytest.empty_queue()

    # Run the test
    await player_message('.menu')

    # Remove embeds and messages 1 through 4. 1=Main Menu; 2=Character Sheet; 3=Selection; 4=Confirm; 5=Confirm Message
    for i in range(0, 5):
        dpytest.sent_queue.get_nowait()

    # Assert expected outputs
    dpytest.verify_message(f"{name} has used their free profession slot to become a '**Weaver**'")
    dpytest.verify_embed(exp_embed, allow_text=True, full=True)

@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
@mock.patch('cogs.utils.workshop.ask_for_quantity')
@pytest.mark.asyncio
async def test_craft_item(mock_ask_for_quantity, mock_wait_for_reply, player_message):
    # Define expectations
    exp_embed = test_data.get_character_sheet_embed('player', level=True, free_profession=True)

    # Define mocks to open menus
    # Order of user inputs:
    #   2 - Workshop
    #   1 - Create a mundane item
    #   1 - Select Weaver Skill
    #   1 - Select "Adventure Gear"
    #   1 - Select "Basket"
    #   3 - Mocked via ask_for_quantity - makes 3 baskets
    #   1 - Confirm choice
    replies = deque(['2', '1', '1', '1', '1', '1', 'exit'])
    quantity_replies = deque([3])
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)
    mock_ask_for_quantity.side_effect = helper.make_side_effect_from_deque(quantity_replies)

    # Clear previous output
    await dpytest.empty_queue()

    # Run the test
    await player_message('.menu')

    # Remove messages for menus we don't care about
    for i in range(0, 7):
        dpytest.sent_queue.get_nowait()

    # Assert expected outputs
    dpytest.verify_message("player successfully crafted 3x**Basket** for **0.60gp**!")

    # Check that the market menu has updated with new gold and worker limit
    new_market_embed = dpytest.get_embed()
    helper.embed_matches_field(name="Gold", value="9.40", embed=new_market_embed)
    helper.embed_matches_field(name="Current Weekly Limit", value="49.40", embed=new_market_embed)






