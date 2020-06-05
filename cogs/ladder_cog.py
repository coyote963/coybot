# -*- coding: utf-8 -*-

from discord.ext import commands
from cogs.toplist import tdm_rankings, dm_rankings, ctf_rankings
from cogs.secrets import uri
from pymongo import MongoClient, collection
import discord
import asyncio
from cogs.ladder_function import get_standings
from cogs.secrets import uri
from tabulate import tabulate

class Ladder(commands.Cog):
    """This part of the bot is for checking your ratings"""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient(uri).bmdb

    @commands.command()
    async def ladder(self, ctx, page : str = "1"):
        """Check the Ladder leaderboard"""
        await ctx.send('Current Ladder Standings: Page {}'.format(page))
        rankings = get_standings(self.db, int(page))
        result = tabulate(rankings, headers="keys")
        if rankings != []:
            await ctx.send( "```{}```".format(result))
        else:
            await ctx.send("No data on page {} :(".format(page))


def setup(bot):
    bot.add_cog(Ladder(bot))
