import logging
import pytest
import discord.ext.test as dpytest
import bot

log = logging.getLogger(__name__)

@pytest.fixture()
def testbot():
    log.debug("Setting up testbot")
    testbot = bot.TestBot()
    for cog in testbot.initial_extensions:
        testbot.load_extension(cog)
    dpytest.configure(testbot)
    config = dpytest.get_config()
    yield testbot