import io
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands

from bot import SelfBot


async def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')


class REPL:
    def __init__(self, bot: SelfBot):
        self.bot = bot
        self._last_result = None

    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = await cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send('```py\n{0.__class__.__name__}: {0}\n```'.format(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                await ctx.send('```py\n%s%s\n```' % (value, ret))


def setup(bot):
    bot.add_cog(REPL(bot))
