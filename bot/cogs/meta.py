import datetime

from discord.ext import commands

from bot import SelfBot


class Meta:
    def __init__(self, bot: SelfBot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx: commands.Context):
        """Closes the bot safely"""

        await ctx.message.delete()
        await self.bot.logout()

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """Tells you how long the bot has been up for"""

        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt

        await ctx.message.edit(content='Uptime: **{}**'.format(fmt.format(d=days, h=hours, m=minutes, s=seconds)))

    @commands.command()
    async def clean(self, ctx: commands.Context, limit: int = 100):
        """Purge messages in the current channel. Default limit is 100 messages"""

        deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == self.bot.user.id)
        await ctx.send(content=f'Deleted {len(deleted)} messages', delete_after=5)

    @commands.command(name='reload')
    async def _reload(self, ctx, *, ext: str = None):
        """Reloads a module."""

        if ext:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
        else:
            for m in self.bot.initial_extensions:
                self.bot.unload_extension(m)
                self.bot.load_extension(m)

    async def __error(self, ctx: commands.Context, error):
        await ctx.message.edit(content=f'Failed to execute command!\n{type(error).__name__}: {error}')

    async def __after_invoke(self, ctx: commands.Context):
        try:
            await ctx.message.add_reaction('👌')
        except:
            pass


def setup(bot):
    bot.add_cog(Meta(bot))
