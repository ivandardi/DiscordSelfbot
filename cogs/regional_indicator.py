from discord.ext import commands

from bot import SelfBot


class RegionalIndicator:
    def __init__(self, bot: SelfBot):
        self.bot = bot
        self.numbers = (
            ':zero:',
            ':one:',
            ':two:',
            ':three:',
            ':four:',
            ':five:',
            ':six:',
            ':seven:',
            ':eight:',
            ':nine:',
        )

    @commands.command()
    async def ri(self, ctx: commands.Context, *, msg: str):
        """Makes the whole message into regional_indicator emojis"""

        def convert(c):
            if c.isalpha():
                return f'\u200b:regional_indicator_{c.lower()}:\u200b'
            if c.isdigit():
                return f'\u200b{self.numbers[int(c)]}\u200b'
            return c

        new_msg = ''.join(map(convert, msg))

        await ctx.message.edit(content=new_msg)


def setup(bot):
    bot.add_cog(RegionalIndicator(bot))
