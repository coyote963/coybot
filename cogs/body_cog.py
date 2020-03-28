# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import requests
import json
import random
from cogs.secrets import username, password
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

    @commands.command()
    async def boringmeme(self, ctx, *query):
        """Takes a random chat message that a boringman player has said and makes a meme out of it"""
        templates = [
            '188390779',
            '61532',
            '91538330',
            '8072285',
            '124055727',
            '61546',
            '232391043',
            '232395549',
            '232396265',
            '232396265',
            '61582',
            '114585149',
            '14230520',
            '101511',
            '14230520',
            '123999232',
            '438680',
            '87743020',
            '61579',
            '181913649',
            '102156234',
            '61556',
            '235589',
            '84341851',
            '61580',
            '232389371'
        ]
        response = requests.request("GET", "https://rest.bman.gg/chat/random")
        message0 = json.loads(response.text)[0]['message']
        message1 = json.loads(response.text)[1]['message']
        url = "https://api.imgflip.com/caption_image"

        payload = {'template_id': '41754803',
            'text0': message0,
            'text1': message1,
            'username': username,
            'password': password,
            'template_id': random.choice(templates),
        }
        files = [

        ]
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        await(ctx.send(json.loads(response.text)['data']['url']))

def setup(bot):
    bot.add_cog(Body(bot))
