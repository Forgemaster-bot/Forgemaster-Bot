from discord.ext import commands
from bot import Forgemaster
import asyncio
import uvloop
import contextlib
import logging

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@contextlib.contextmanager
def setup_logging():
    """
    Setup logging via context manager.
    Credit: https://github.com/Rapptz/RoboDanny/blob/rewrite/launcher.py
    """
    try:
        # __enter__
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='Forgemaster.log', encoding='utf-8', mode='w')
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)
        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


def main():
    """
    Sets up logging and launches the bot
    :return:
    """
    # Make sure event loop has been created
    loop = asyncio.get_event_loop()
    with setup_logging():
        # Start bot and run event loop
        bot = Forgemaster()
        bot.run()


if __name__ == '__main__':
    main()

