from discord.ext import commands
from bot import TestBot
import asyncio
import contextlib
import logging
from datetime import datetime

# Use uvloop if it is installed
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Not using uvloop as it is not installed...")

use_log_timestamp = True

def setup_logging():
    # __enter__
    logging.getLogger('discord').setLevel(logging.INFO)
    logging.getLogger('discord.http').setLevel(logging.WARNING)

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # Define log format
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')

    # Add file logger
    file_prefix = "bot"
    if use_log_timestamp:
        file_prefix = f"{file_prefix}{datetime.now().strftime('_%H_%M_%d_%m_%Y')}"
    filename = f"{file_prefix}.log"
    handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
    handler.setFormatter(fmt)
    log.addHandler(handler)

    # Add stdout logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    log.addHandler(console_handler)


def shutdown_logging():
    # __exit__
    log = logging.getLogger()
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


@contextlib.contextmanager
def logging_enabled():
    """
    Setup logging via context manager.
    Credit: https://github.com/Rapptz/RoboDanny/blob/rewrite/launcher.py
    """
    try:
        setup_logging()
        yield
    finally:
        shutdown_logging()


def main():
    """
    Sets up logging and launches the bot
    :return:
    """
    # Make sure event loop has been created
    loop = asyncio.get_event_loop()
    with logging_enabled():
        # Start bot and run event loop
        bot = TestBot()
        bot.run()


if __name__ == '__main__':
    main()

