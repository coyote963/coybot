# -*- coding: utf-8 -*-

from discord.ext import commands
from cogs.search_function import get_player, get_steam_profile, get_hex_code, get_hex
from cogs.secrets import uri
from pymongo import MongoClient
from cogs.game_ids import hats, premium, store
import discord
import asyncio

class Search(commands.Cog):
    """This part of the bot is for returning search"""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient(uri).bmdb

    @commands.command()
    async def profile(self, ctx, query: str = ""):
        """Sends the profile of the username provided"""
        if len(query) != 0:
            player = get_player(self.db, query)
            if player is None:
                await ctx.send("Please check your spelling")
            else:
                alternate_names = []
                for i in range(1, len(player['name'])):
                    alternate_names.append(player['name'][i])
                embed = discord.Embed(
                    title = player['name'][0],
                    description = "aliases : " + str(alternate_names),
                    colour = get_hex_code(get_hex(int(player['color']))),
                    url = "https://steamcommunity.com/profiles/{}".format(player['_id']['profile'])
                )
                
                profile = get_steam_profile(player)
                if 'premium' in player:
                    embed.add_field(name="status", value = premium[int(player['premium'])])
                embed.add_field(name="hat", value=hats[int(player['hat'])])
                embed.add_field(name="platform", value = store[int(player['_id']['platform'])])
                embed.set_image(url =  profile['response']['players'][0]['avatarfull'])
                await ctx.send(embed = embed)
        else:
            await ctx.send("Provide a username")


def setup(bot):
    bot.add_cog(Search(bot))
