import logging
import pytest
import discord.ext.test as dpytest
import tests.test_data.test_menu_data as test_menu_data


log = logging.getLogger(__name__)

@pytest.yield_fixture(scope='module')
def event_loop(request):
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def testbot(request):
    """ This fixture sets up a discordbot object for each test case. """
    import bot
    log.debug("Setting up testbot")
    # initial_extensions = bot.TestBot.initial_extensions
    # bot.TestBot.initial_extensions = []
    testbot = bot.TestBot()
    # for cog in testbot.initial_extensions:
    #     testbot.load_extension(cog)
    #     testbot.add_cog(cog)
    cog = testbot.get_cog('Auction')
    cog.update_auctions.cancel()
    dpytest.configure(testbot)
    config = dpytest.get_config()

    yield testbot

    # log.debug("Tearing down testbot")
    # loop = testbot.loop
    # loop.run_until_complete(testbot.close())


@pytest.fixture(scope="module")
async def player_member(testbot):
    from discord.ext.test import backend, get_config
    yield backend.make_member(
            backend.make_user(**test_menu_data.discord_info_lookup['player']), get_config().guilds[0]
        )

@pytest.fixture(scope="module")
async def player_message(player_member):
    import functools
    from discord.ext.test import message
    yield functools.partial(message, member=player_member)

@pytest.fixture(scope="module")
async def admin_member(testbot):
    from discord.ext.test import backend, get_config
    yield backend.make_member(
            backend.make_user(**test_menu_data.discord_info_lookup['admin']),
            get_config().guilds[0],
            roles=[backend.make_role("Admins", get_config().guilds[0], permissions=8)]
        )

@pytest.fixture(scope="module")
async def admin_message(admin_member):
    import functools
    from discord.ext.test import message
    yield functools.partial(message, member=admin_member)

@pytest.fixture(scope="module")
async def nonplayer_member(testbot):
    from discord.ext.test import backend, get_config
    yield backend.make_member(
            backend.make_user(**test_menu_data.discord_info_lookup['non_player']), get_config().guilds[0]
        )

@pytest.fixture(scope="module")
async def nonplayer_message(nonplayer_member):
    import functools
    from discord.ext.test import message
    yield functools.partial(message, member=nonplayer_member)

def setup_characters():
    test_menu_data.create_characters()

@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """ This function is ran only when pytest is started. """
    import launcher
    launcher.setup_logging()
    setup_characters()
    yield
    launcher.shutdown_logging()
