import logging
import discord
import difflib
import pprint
import discord.ext.test as dpytest
from collections import deque
import datetime
import pytz


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

def make_side_effect_wait_for_reply(replies: deque):
    async def mock_wait_for_reply(*args, **kwargs) -> MockPayload:
        if len(replies):
            return MockPayload(replies.popleft())
        return MockPayload('exit')
    return mock_wait_for_reply


def make_side_effect_datetime_now(year, month, day, hour=0, minute=0, second=0, microsecond=0):
    def mocked_get_now(_, tz=pytz.timezone('GMT')):
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                 microsecond=microsecond, tzinfo=tz)
    return mocked_get_now
