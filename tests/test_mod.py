import logging
from collections import deque

import pytest
import mock

# Our modules
import tests.test_data.test_menu_data as test_data
from cogs import auction
from tests import helper
from Character.Character import Character

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
@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
async def test_ticket_cancelled(mock_wait_for_reply, admin_message):
    replies = deque(['2'])
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)

    # Get initial values
    character = Character(test_data.character_info_lookup['player']['character_id'])
    gold, xp = character.gold, character.xp

    # Run the test
    await admin_message('.ticket player/Gold:10,XP:10,Blue Dust:10,Red Dust,Weavers Tools:-1')

    # Lookup the player we were adding an exit ticket for
    character = Character(test_data.character_info_lookup['player']['character_id'])

    # Assert original items
    assert character.gold == gold
    assert character.xp == xp
    # Assert default items
    assert character.items['Weavers Tools'].quantity == 1
    # Assert no new items were added
    with pytest.raises(KeyError):
        assert character.items['Blue Dust'].quantity == 0
    with pytest.raises(KeyError):
        assert character.items['Red Dust'].quantity == 0

@pytest.mark.asyncio
async def test_ticket_error(admin_message):
    # Get initial values
    character = Character(test_data.character_info_lookup['player']['character_id'])
    gold, xp = character.gold, character.xp

    # Run the test
    await admin_message('.ticket player/Gold:-11,XP:10,Blue Dust:10,Red Dust,Weavers Tools:-1')

    # Lookup the player we were adding an exit ticket for
    character = Character(test_data.character_info_lookup['player']['character_id'])

    # Assert original items
    assert character.gold == gold
    assert character.xp == xp
    # Assert default items
    assert character.items['Weavers Tools'].quantity == 1
    # Assert no new items were added
    with pytest.raises(KeyError):
        assert character.items['Blue Dust'].quantity == 0
    with pytest.raises(KeyError):
        assert character.items['Red Dust'].quantity == 0

@pytest.mark.asyncio
@mock.patch('cogs.utils.textmenus.Menu.wait_for_reply')
async def test_ticket_success(mock_wait_for_reply, admin_message):
    replies = deque(['1'])
    mock_wait_for_reply.side_effect = helper.make_side_effect_wait_for_reply(replies)

    # Get initial values
    character = Character(test_data.character_info_lookup['player']['character_id'])
    gold, xp = character.gold+10, character.xp+10

    # Run the test
    await admin_message('.ticket player/Gold:10,XP:10,Blue Dust:10,Red Dust,Weavers Tools:-1')
    # helper.print_current_queue()

    # Lookup the player we were adding an exit ticket for
    character = Character(test_data.character_info_lookup['player']['character_id'])

    # Assert gold, xp, and items were added
    assert character.gold == gold
    assert character.xp == xp
    assert character.items['Blue Dust'].quantity == 10
    assert character.items['Red Dust'].quantity == 1

    # Assert item was removed successfully
    with pytest.raises(KeyError):
        assert character.items['Weavers Tools'].quantity == 0
