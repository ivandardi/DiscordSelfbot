import re

from discord.ext import commands


class RegionalIndicator:
    def __init__(self):
        self.characters = {
            'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}',
            'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
            'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
            'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}',
            'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
            'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
            'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}',
            'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
            'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
            'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}',
            'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
            'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
            'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}',
            'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
            'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
            'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}',
            'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
            'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
            's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}',
            't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
            'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
            'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}',
            'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
            'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
            'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
            'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
            '0': '0\N{COMBINING ENCLOSING KEYCAP}',
            '1': '1\N{COMBINING ENCLOSING KEYCAP}',
            '2': '2\N{COMBINING ENCLOSING KEYCAP}',
            '3': '3\N{COMBINING ENCLOSING KEYCAP}',
            '4': '4\N{COMBINING ENCLOSING KEYCAP}',
            '5': '5\N{COMBINING ENCLOSING KEYCAP}',
            '6': '6\N{COMBINING ENCLOSING KEYCAP}',
            '7': '7\N{COMBINING ENCLOSING KEYCAP}',
            '8': '8\N{COMBINING ENCLOSING KEYCAP}',
            '9': '9\N{COMBINING ENCLOSING KEYCAP}',
            '?': '\N{BLACK QUESTION MARK ORNAMENT}',
            '!': '\N{HEAVY EXCLAMATION MARK SYMBOL}',
        }

    @commands.command()
    async def ri(self, ctx: commands.Context, *, msg: str):
        """Makes the whole message into regional_indicator emojis"""

        def mapper(s: str):
            if s.startswith('<'):
                return s
            return '\u200b'.join(self.characters.get(c.lower(), c) for c in s)

        strings = re.split(r"(<\S*>)", msg)

        new_msg = ''.join(map(mapper, strings))

        await ctx.message.edit(content=new_msg)


def setup(bot):
    bot.add_cog(RegionalIndicator())
