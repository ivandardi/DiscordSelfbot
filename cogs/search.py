import json
import logging

import aiohttp
from discord.ext import commands

from bot import SelfBot

log = logging.getLogger('selfbot')


class Results(object):
    def __init__(self, response):
        self.type = {
            'A': 'answer',
            'D': 'disambiguation',
            'C': 'category',
            'N': 'name',
            'E': 'exclusive',
            '': 'nothing'
        }.get(response.get('Type', ''), '')

        self.response = response
        self.api_version = None  # compat

        self.heading = response.get('Heading', '')

        self.results = [Result(elem) for elem in response.get('Results', [])]
        self.related = [Result(elem) for elem in response.get('RelatedTopics', [])]

        self.abstract = Abstract(response)
        self.redirect = Redirect(response)
        self.definition = Definition(response)
        self.answer = Answer(response)

        self.image = Image({'Result': response.get('Image', '')})


class Abstract(object):
    def __init__(self, response):
        self.html = response.get('Abstract', '')
        self.text = response.get('AbstractText', '')
        self.url = response.get('AbstractURL', '')
        self.source = response.get('AbstractSource')


class Redirect(object):
    def __init__(self, response):
        self.url = response.get('Redirect', '')


class Result(object):
    def __init__(self, response):
        self.topics = response.get('Topics', [])
        if self.topics:
            self.topics = [Result(t) for t in self.topics]
            return
        self.html = response.get('Result')
        self.text = response.get('Text')
        self.url = response.get('FirstURL')

        icon_response = response.get('Icon')
        if icon_response is not None:
            self.icon = Image(icon_response)
        else:
            self.icon = None


class Image(object):
    def __init__(self, response):
        self.url = response.get('Result')
        self.height = response.get('Height', None)
        self.width = response.get('Width', None)


class Answer(object):
    def __init__(self, response):
        self.text = response.get('Answer')
        self.type = response.get('AnswerType', '')


class Definition(object):
    def __init__(self, response):
        self.text = response.get('Definition', '')
        self.url = response.get('DefinitionURL')
        self.source = response.get('DefinitionSource')


class Search:
    def __init__(self, bot: SelfBot):
        self.bot = bot
        self.client = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.client.close()

    @commands.command()
    async def ddg(self, ctx: commands.Context, *, query: str):
        """Searches DuckDuckGo and gives you top result."""

        result = await self.get_zci(query)
        await ctx.message.edit(content=result)

    async def get_zci(self, q):
        """
        A helper method to get a single (and hopefully the best) ZCI result.
        priority=list can be used to set the order in which fields will be checked for answers.
        Use web_fallback=True to fall back to grabbing the first web result.
        passed to query. This method will fall back to 'Sorry, no results.' 
        if it cannot find anything.
        """

        priority = ['answer', 'abstract', 'related.0', 'definition']

        ddg = await self.query(q)
        response = ''

        for p in priority:
            ps = p.split('.')
            type_ = ps[0]
            index = int(ps[1]) if len(ps) > 1 else None

            result = getattr(ddg, type_)
            if index:
                result = result[index] if len(result) > index else None
            if not result:
                continue

            if result.text:
                response = result.text
            if result.text and hasattr(result, 'url') and result.url:
                response += f' ({result.url})'
            if response:
                break

        # if there still isn't anything, try to get the first web result
        if not response:
            if ddg.redirect.url:
                response = ddg.redirect.url

        # final fallback
        if not response:
            response = 'Sorry, no results.'

        return response

    async def query(self, query):
        params = {
            'q': query,
            'format': 'response',
            'no_redirect': '1',
            'no_html': '1',
            'skip_disambig': '1',
            'safesearch': '-1',
            't': 'python-duckduckgo 0.242-ivan',
        }

        url = 'http://api.duckduckgo.com/'
        async with self.client.get(url, params=params) as r:
            response = await r.text()
            response = json.loads(response)

        return Results(response)


def setup(bot):
    bot.add_cog(Search(bot))
