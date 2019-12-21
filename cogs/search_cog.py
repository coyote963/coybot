# -*- coding: utf-8 -*-

from discord.ext import commands
from cogs.search_function import get_profile, get_player, get_steam_profile, get_color_name, get_hex_code, get_hex
from cogs.secrets import uri
from pymongo import MongoClient
from cogs.game_ids import hats, premium, store, steam_status
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
                alternate_names = ""
                for i in range(1, len(player['name'])):
                    alternate_names + player['name'][i]
                if alternate_names == "":
                    alternate_names = "None"
                platform = int(player['_id']['platform'])
                if platform == 0:
                    embed = discord.Embed(
                        title = player['name'][0],
                        description = "aliases : " + alternate_names,
                        colour = get_hex_code(get_hex(int(player['color']))),
                        url = "https://steamcommunity.com/profiles/{}".format(player['_id']['profile'])
                    )
                else:
                    embed = discord.Embed(
                        title = player['name'][0],
                        description = "aliases : " + alternate_names,
                        colour = get_hex_code(get_hex(int(player['color']))),
                    )
                if platform == 0:
                    profile = get_steam_profile(player)
                    embed.set_image(url =  profile['response']['players'][0]['avatarfull'])
                    embed.add_field(name = "Steam Status", value = steam_status[int(profile['response']['players'][0]['personastate'])], inline=False)
                if 'premium' in player:
                    embed.add_field(name="Account", value = premium[int(player['premium'])])
                embed.add_field(name="Hat", value=hats[int(player['hat'])])
                embed.add_field(name="Platform", value = store[int(player['_id']['platform'])])
                embed.add_field(name="Color", value = get_color_name(*get_hex(int(player['color']))))
                has_dm = ":x:" if get_profile(self.db.dm_profiles, player) is None else ":o:"
                has_tdm = ":x:" if get_profile(self.db.tdm_profiles, player) is None else ":o:"
                has_ctf = ":x:" if get_profile(self.db.ctf_profiles, player) is None else ":o:"
                embed.set_footer(text = "dm {} | tdm {} | ctf {}".format(has_dm, has_tdm, has_ctf))
                await ctx.send(embed = embed)
        else:
            await ctx.send("Provide a username")

    @commands.command()
    async def getdm(self, ctx, query: str = ""):
        """Sends information about searched Deathmatch rating"""
        if len(query) == 0:
            await ctx.send("Provide a username")
        else:
            player = get_player(self.db, query)
            
            if player is None:
                await ctx.send("Please check your spelling")
            else:
                alternate_names = ""
                for i in range(1, len(player['name'])):
                    alternate_names + player['name'][i]
                
                profile = get_profile(self.db.dm_profiles, player)
                if profile is not None:
                    platform = int(player['_id']['platform'])
                    if platform == 0:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description = "Deathmatch Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                            url = "https://steamcommunity.com/profiles/{}".format(player['_id']['profile'])
                        )
                    else:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description =  "Deathmatch Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                        )

                    embed.add_field(name="K/D", value="{}/{}".format(profile['kills'], profile['deaths']))
                    embed.add_field(name="Mu", value="{}".format(round(float(profile['mu']), 2)))
                    embed.add_field(name="Sigma", value="{}".format(round(float(profile['sigma']), 2)))
                    embed.add_field(name="Rating", value="{}".format(round(float(profile['mu']) - 3 * float(profile['sigma']), 2)))
                    embed.add_field(name="Last Updated", value="{} UTC".format(profile['last_updated']))
                    
                    if platform == 0:
                        profile = get_steam_profile(player)
                        embed.set_image(url =  profile['response']['players'][0]['avatarfull'])
                        embed.add_field(name = "Steam Status", value = steam_status[int(profile['response']['players'][0]['personastate'])], inline=False)

                    await ctx.send(embed = embed)
                else:
                    await ctx.send("There is no data or rating information for this person. Check back later")

    @commands.command()
    async def getctf(self, ctx, query: str = ""):
        """Sends information about searched ctf rating"""
        if len(query) == 0:
            await ctx.send("Provide a username")
        else:
            player = get_player(self.db, query)
            
            if player is None:
                await ctx.send("Please check your spelling")
            else:
                alternate_names = ""
                for i in range(1, len(player['name'])):
                    alternate_names + player['name'][i]
                
                profile = get_profile(self.db.ctf_profiles, player)
                if profile is not None:
                    platform = int(player['_id']['platform'])
                    if platform == 0:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description = "Capture the Flag Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                            url = "https://steamcommunity.com/profiles/{}".format(player['_id']['profile'])
                        )
                    else:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description =  "Capture the Flag Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                        )

                    embed.add_field(name="Mu", value="{}".format(round(float(profile['mu']), 2)))
                    embed.add_field(name="Sigma", value="{}".format(round(float(profile['sigma']), 2)))
                    embed.add_field(name="Rating", value="{}".format(round(float(profile['mu']) - 3 * float(profile['sigma']), 2)))
                    embed.add_field(name="Last Updated", value="{} UTC".format(profile['last_updated']))
                    if platform == 0:
                        profile = get_steam_profile(player)
                        embed.set_image(url =  profile['response']['players'][0]['avatarfull'])
                        embed.add_field(name = "Steam Status", value = steam_status[int(profile['response']['players'][0]['personastate'])], inline=False)

                    await ctx.send(embed = embed)
                else:
                    await ctx.send("There is no data or rating information for this person. Check back later")

    
    @commands.command()
    async def gettdm(self, ctx, query: str = ""):
        """Sends information about searched tdm rating"""
        if len(query) == 0:
            await ctx.send("Provide a username")
        else:
            player = get_player(self.db, query)
            
            if player is None:
                await ctx.send("Please check your spelling")
            else:
                alternate_names = ""
                for i in range(1, len(player['name'])):
                    alternate_names + player['name'][i]
                
                profile = get_profile(self.db.tdm_profiles, player)
                if profile is not None:
                    platform = int(player['_id']['platform'])
                    if platform == 0:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description = "Team Deathmatch Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                            url = "https://steamcommunity.com/profiles/{}".format(player['_id']['profile'])
                        )
                    else:
                        embed = discord.Embed(
                            title = player['name'][0],
                            description =  "Team Deathmatch Profile [{}]".format(alternate_names),
                            colour = get_hex_code(get_hex(int(player['color']))),
                        )
                    embed.add_field(name="K/D", value="{}/{}".format(profile['kills'], profile['deaths']))
                    embed.add_field(name="W/L", value="{}/{}".format(profile['wins'], profile['losses']))
                    embed.add_field(name="Mu", value="{}".format(round(float(profile['mu']), 2)))
                    embed.add_field(name="Sigma", value="{}".format(round(float(profile['sigma']), 2)))
                    embed.add_field(name="Rating", value="{}".format(round(float(profile['mu']) - 3 * float(profile['sigma']), 2)))
                    embed.add_field(name="Last Updated", value="{} UTC".format(profile['last_updated']))
                    if platform == 0:
                        profile = get_steam_profile(player)
                        embed.set_image(url =  profile['response']['players'][0]['avatarfull'])
                        embed.add_field(name = "Steam Status", value = steam_status[int(profile['response']['players'][0]['personastate'])], inline=False)

                    await ctx.send(embed = embed)
                else:
                    await ctx.send("There is no data or rating information for this person. Check back later")

def setup(bot):
    bot.add_cog(Search(bot))
