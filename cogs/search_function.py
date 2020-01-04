import requests
import re
from cogs.secrets import steam_key
def get_hex(colorvalue):
    b = int(colorvalue / (256 ** 2))
    remainder = colorvalue % (256 ** 2)
    g = int(remainder / 256)
    r = remainder % 256
    return (r,g,b)

def get_hex_code(color_tuple):
    return color_tuple[0] << 16 | color_tuple[1] << 8 | color_tuple[2]

def get_color_name(r,g,b):
    response = requests.get("https://www.thecolorapi.com/id?rgb=rgb({},{},{})".format(r, g, b))
    if (r, g, b) == (255, 0, 255):
        return "M a g en t a"
    return response.json()['name']['value']

def get_player(db, query):
    player = db.players.find_one(
        {'name' : {'$regex' : re.compile(re.escape(query), re.IGNORECASE)}})
    if player is not None:
        return player

def get_steam_profile(player):
    if player['_id']['platform'] == '0':
        steam_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(steam_key,player['_id']['profile'])
        response = requests.get(steam_url)
        return response.json()


def get_profile(collection, player):
    return collection.find_one(
        {'player' : player['_id']}
    )
