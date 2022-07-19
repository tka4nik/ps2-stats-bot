# bot.py
import os
import random
import time
import requests
import discord
from dotenv import load_dotenv
import cProfile

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')

intents = discord.Intents.default()  # Gets the default intents from discord.
intents.members = True  # enables members intents on the bot.

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='99', help='Random quote')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

def get_server_data(servers):
    servers_data = {}
    for server_id in servers.keys():
        servers_data[server_id] = requests.get(
            'https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8'.format(SERVICE_ID,
                                                                                                         server_id)
        ).json()
    return servers_data

@bot.command(name='c', help='Open continents')
async def open_continents(ctx):
    start_time = time.time()
    continents = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'], 6: ['6001', '6002', '6003'],
                  8: ['18029', '18030', '18062']}
    zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir"}
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}
    output = ""
    servers_data = get_server_data(servers)

    print("---Requests: %s seconds ---" % (time.time() - start_time))
    for server_id in servers_data:
        request = servers_data[server_id]
        for continent in request['map_list']:
            factions = set()
            for region in continent['Regions']['Row']:
                if region['RowData']['RegionId'] in continents[int(continent['ZoneId'])]:
                    factions.add(int(region['RowData']['FactionId']))
            if len(factions) == 3:
                output += "{0}: {1}\n".format(servers[server_id], zones[int(continent['ZoneId'])])
    print(output)
    print("---Parsing: %s seconds ---" % (time.time() - start_time))
    await ctx.send(output)

bot.run(TOKEN)
