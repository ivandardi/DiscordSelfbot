import datetime
import logging
import os
import traceback

import discord
from discord.ext import commands


def setup_logging():
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')

    handler = logging.FileHandler(filename='logging.log', encoding='utf-8', mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)

    return logger


log = setup_logging()


class SelfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime = datetime.datetime.utcnow()
        self.initial_extensions = [
            'bot.cogs.meta',
            'bot.cogs.regional_indicator',
            'bot.cogs.repl',
            'bot.cogs.slashes',
        ]

        for extension in self.initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_command_error(self, ctx, error):
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        log.error(f'Command error in %s:\n%s', ctx.command.qualified_name, tb)

    async def on_command(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            destination = f'#{ctx.channel}'
        else:
            destination = f'#{ctx.channel} ({ctx.guild})'

        log.info(f'%s: %s', destination, ctx.message.content)


def main():
    bot = SelfBot(
        self_bot=True,
        command_prefix=['.', '/', 'me.'],
    )

    bot.run(os.environ['TOKEN_DISCORD'], bot=False)

    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
