from discord.ext import commands

from bot import SelfBot


class Slashes:
    def __init__(self, bot: SelfBot):
        self.bot = bot

    @commands.command()
    async def tableflip(self, ctx: commands.Context):
        """(╯°□°）╯︵ ┻━┻"""

        await ctx.message.edit(content=ctx.message.content[10:] + ' (╯°□°）╯︵ ┻━┻')

    @commands.command()
    async def unflip(self, ctx: commands.Context):
        """┬──┬﻿ ノ( ゜-゜ノ)"""

        await ctx.message.edit(content=ctx.message.content[7:] + ' ┬──┬﻿ ノ( ゜-゜ノ)')

    @commands.command()
    async def justright(self, ctx: commands.Context):
        """✋😩👌"""

        await ctx.message.edit(content=ctx.message.content[10:] + ' ✋😩👌')

    @commands.command()
    async def shrug(self, ctx: commands.Context):
        """¯\\_(ツ)_/¯"""

        await ctx.message.edit(content=ctx.message.content[6:] + ' ¯\\_(ツ)_/¯')

    @commands.command()
    async def lenny(self, ctx: commands.Context):
        """( ͡° ͜ʖ ͡°)"""

        await ctx.message.edit(content=ctx.message.content[6:] + ' ( ͡° ͜ʖ ͡°)')

    @commands.command()
    async def wtf(self, ctx: commands.Context):
        """ಠ_ಠ"""

        await ctx.message.edit(content=ctx.message.content[4:] + ' ಠ_ಠ')

    @commands.command()
    async def me(self, ctx: commands.Context):
        """**woo**"""

        await ctx.message.edit(content='**' + ctx.message.content[4:] + '**')


def setup(bot):
    bot.add_cog(Slashes(bot))
