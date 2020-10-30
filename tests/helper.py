import logging
import discord
import difflib
import pprint
import discord.ext.test as dpytest
from collections import deque
import datetime
import pytz
from asyncio.queues import QueueEmpty
from Exceptions import ExitException


log = logging.getLogger(__name__)


def log_and_compare_message(left_msg, right_msg):
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

def wait_until_menu(title: str):
    import time
    time.sleep(4)

class MockPayload:
    def __init__(self, content: str):
        self.content: str = content
        self.author = None

def make_side_effect_wait_for_reply(replies: deque):
    async def mock_wait_for_reply(*args, **kwargs) -> MockPayload:
        if len(replies):
            return MockPayload(replies.popleft())
        return MockPayload('exit')
    return mock_wait_for_reply

def make_side_effect_from_deque(replies: deque):
    async def mock_wait_for_reply(*args, **kwargs):
        if len(replies):
            return replies.popleft()
        raise ExitException
    return mock_wait_for_reply


def make_side_effect_datetime_now(year, month, day, hour=0, minute=0, second=0, microsecond=0):
    def mocked_get_now(_, tz=pytz.timezone('GMT')):
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                 microsecond=microsecond, tzinfo=tz)
    return mocked_get_now


def print_current_queue():
    i = 0
    while True:
        item = None
        try:
            item = dpytest.sent_queue.get_nowait()
            # Try to get top of queue by peeking this will throw an error if its not an embed
            output = '\n'.join(pprint.pformat(item.embeds[0].to_dict()).splitlines())
            log.debug(f"Embed #{i}: {output}")
            # TODO: Probably a better way to do this
        except QueueEmpty:
            log.debug(f"Total number in queue: {i}")
            break
        except:
            log.debug(f"Message #{i}: {item.content}")
        i = i + 1


def embed_matches_field(name: str, value: str, embed):
    """Returns true if an embed's field matches the given name and value"""
    data = embed.to_dict()
    for field in data['fields']:
        if field['name'] == name:
            assert field['value'] == value, \
                f"Field '{name}' did not contain matching value. Got: '{field['value']}'. Exp: '{value}'."
    return False
