# -*- coding: utf-8 -*-

from discord.ext import commands
from cogs.toplist import tdm_rankings, dm_rankings, ctf_rankings
from cogs.secrets import uri
from pymongo import MongoClient
import discord
import asyncio



class Ratings(commands.Cog):
    """This part of the bot is for checking your ratings"""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient(uri).bmdb

    @commands.command()
    async def ctf(self, ctx, sort: str = ""):
        """Check the CTF Leaderboards"""
        await ctx.send('CTF leaderboard')
        rankings = ctf_rankings(self.db)
        await ctx.send('{}'.format(rankings))

    @commands.command()
    async def tdm(self, ctx, sort: str = ""):
        """Check the TDM leaderboards"""
        await ctx.send('TDM leaderboard {}'.format(sort))
        rankings = tdm_rankings(self.db)
        await ctx.send('{}'.format(rankings))

    @commands.command()
    async def dm(self, ctx, sort: str = ""):
        """Check the DM leaderboards"""
        await ctx.send('DM leaderboard {}'.format(sort))
        rankings = dm_rankings(self.db)
        await ctx.send('{}'.format(rankings))

def setup(bot):
    bot.add_cog(Ratings(bot))
