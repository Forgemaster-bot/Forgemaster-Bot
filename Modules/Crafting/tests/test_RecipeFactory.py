import unittest
from unittest.mock import patch
import asyncio

import Crafting.Crafting
import Crafting.Utils
import Crafting.Parser
import Crafting.RecipeFactory
import Character.Character
import Connections

from Crafting.Utils import ExitException


sent_messages = []
replies = []


async def mock_send_message(context, message):
    sent_messages.append(message)
    print(message)


async def mock_wait_for_reply(cog, context):
    if len(replies):
        return replies.pop()
    else:
        raise ExitException()


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class MockBot:
    def get_channel(self, id):
        return None


class MockCog:
    bot = MockBot()




character_id = "E4CEFA15-B3C7-4B6E-8EA9-DC140B5D0338"
file_label = 'thaumstyn'

class MyTestCase(unittest.TestCase):

    # @patch('Crafting.Utils.send_message', side_effect=mock_send_message)
    # @patch('Crafting.Utils.wait_for_reply', side_effect=mock_wait_for_reply)
    # def test_mocks(self, mock_msg, mock_reply):
    #     event_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(event_loop)
    #
    #     async def run_test():
    #         global replies
    #         global sent_messages
    #
    #         sent_messages.clear()
    #         await Crafting.Utils.send_message(None, "Test")
    #         # self.assertTrue(len(sent_messages) == 1)
    #         assert (len(sent_messages) == 1)
    #         sent_messages.clear()
    #
    #         replies = ["test"]
    #         await Crafting.Utils.wait_for_reply(None, "Test")
    #         # self.assertTrue(len(replies) == 0)
    #         assert (len(replies) == 0)
    #
    #     # Run the async test
    #     coro = asyncio.coroutine(run_test)
    #     event_loop.run_until_complete(coro())
    #     event_loop.close()

    @patch('Crafting.Utils.send_message', side_effect=mock_send_message)
    @patch('Crafting.Utils.wait_for_reply', side_effect=mock_wait_for_reply)
    @patch('Update_Google_Roster.update_character_in_roster')
    def test_magic_item_crafting(self, mock_msg, mock_reply, mock_update):

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        async def run_test():
            global replies
            global sent_messages

            exp_recipe_name = "Leather Armor of Gleaming"
            exp_message = "1 : Leather Armor of Gleaming"
            replies = ['2', '2', '1', '1', '1', 'Yes']
            replies.reverse()
            sent_messages.clear()

            data = Crafting.Parser.parse_file(file_label)['recipes']
            assert(data is not None)
            recipe = await Crafting.Utils.ask_user_to_select_recipe(None, None, data, file_label)
            assert(recipe.name == exp_recipe_name)
            sent_messages.clear()

            character = Character.Character.Character(character_id)
            # random_outcome success range
            with patch('random.randint', return_value=100) as mock_random:
                exp_message1 = "You rolled '100'."
                exp_message2 = f"You successfully crafted **1x[{exp_recipe_name}]**"
                await Crafting.Crafting.craft_recipe(MockCog(), None, character, recipe)
                assert(any([True for msg in sent_messages if exp_message1 in msg]))
                assert (any([True for msg in sent_messages if exp_message2 in msg]))

            # random_outcome slot range
            with patch('random.randint', return_value=70) as mock_random:
                exp_message1 = "You rolled '70'."
                exp_message2 = f"You successfully crafted **1x["

                await Crafting.Crafting.craft_recipe(MockCog(), None, character, recipe)
                assert (any([True for msg in sent_messages if exp_message1 in msg]))
                assert (any([True for msg in sent_messages if exp_message2 in msg]))

            # random_outcome rarity range
            with patch('random.randint', return_value=30) as mock_random:
                exp_message1 = "You rolled '30'."
                exp_message2 = f"You successfully crafted **1x["

                await Crafting.Crafting.craft_recipe(MockCog(), None, character, recipe)
                assert (any([True for msg in sent_messages if exp_message1 in msg]))
                assert (any([True for msg in sent_messages if exp_message2 in msg]))

            # random_outcome failure range
            with patch('random.randint', return_value=5) as mock_random:
                exp_message1 = "You rolled '5'."
                exp_message2 = f"Crafting failed"

                await Crafting.Crafting.craft_recipe(MockCog(), None, character, recipe)
                assert (any([True for msg in sent_messages if msg if exp_message1 in msg]))
                assert (any([True for msg in sent_messages if msg if exp_message2 in msg]))

        # Run the async test
        coro = asyncio.coroutine(run_test)
        event_loop.run_until_complete(coro())
        event_loop.close()


if __name__ == '__main__':
    unittest.main()
