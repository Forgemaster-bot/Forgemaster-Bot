import logging
import pytest
# import discord.ext.test as dpytest
import discord.ext.test
import bot
import launcher

log = logging.getLogger(__name__)

# @pytest.fixture()
# def testbot():
#     log.debug("Setting up Forgemaster")
#     testbot = bot.TestBot()
#     for cog in testbot.initial_extensions:
#         testbot.load_extension(cog)
#     dpytest.configure(testbot)
#     config = dpytest.get_config()
#     yield testbot
