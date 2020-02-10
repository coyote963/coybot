# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio


class Body(commands.Cog):
    """This part of the bot is for returning search"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbody(self,ctx, *query):
        """Sets the game presence of the bot"""
        query = " ".join(query)
        """Sets the body of this bot to the query"""
        if len(query) == 0:
            await ctx.send("Provide a username")
        else:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(query))

def setup(bot):
    bot.add_cog(Body(bot))
