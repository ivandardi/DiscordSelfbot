import datetime
import json
import logging
import traceback

import discord
from discord.ext import commands


def setup_logger(name: str):
    handler = logging.FileHandler(filename='logging.log', encoding='utf-8', mode='w')

    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(module)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
log = setup_logger('selfbot')


class SelfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.uptime = None

        self.initial_extensions = [
            'cogs.meta',
            'cogs.regional_indicator',
            'cogs.repl',
            'cogs.search',
            'cogs.slashes',
        ]

        with open('credentials.json') as f:
            self.credentials = json.load(f)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        if not self.uptime:
            self.uptime = datetime.datetime.utcnow()

    async def on_command_error(self, exception, context):
        log.error(f'Command error in {context.command}:')
        traceback.print_tb(exception.original.__traceback__)
        log.error('{0.__class__.__name__}: {0}'.format(exception.original))

    async def on_command(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            destination = 'Private Message'
        else:
            destination = f'#{ctx.channel.name} ({ctx.guild.name})'

        log.info(f'{destination}: {ctx.message.content}')


if __name__ == '__main__':

    bot = SelfBot(
        self_bot=True,
        command_prefix=['.', '/', 'me.'],
        help_attrs=dict(hidden=True),
    )

    for extension in bot.initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(bot.credentials['token'], bot=False)

    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)