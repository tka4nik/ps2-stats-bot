# bot.py
import os
import random
import time
import datetime
import requests
import discord
from dotenv import load_dotenv
import aiohttp
import asyncio
from discord.ext import commands

load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')

intents = discord.Intents.default()  # Gets the default intents from discord.
intents.members = True  # enables members intents on the bot.

bot = commands.Bot(command_prefix='!', intents=intents)
session = requests.Session()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    print(error)
    print(ctx.command)
    print(discord.HTTPException)
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('Command not found!')
    if isinstance(error, discord.ext.commands.CommandInvokeError):
        if "400" in str(error):
            await ctx.send('No continents are open at the moment/the servers are down!')
        else:
            await ctx.send('Something wrong has happened!')
    with open("log/err.log", "a+") as f:
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(error) + "\n")


def get_tasks(session, servers):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8,344".format(SERVICE_ID, server_id)) for server_id in servers.keys()]
    return tasks


async def get_data(servers):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, servers)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, server_id in zip(responses, servers):
            results[server_id] = await response.json()
        return results


def get_server_data_dummy(servers):
    return ""


@bot.command(name='c', help='Open continents')
async def open_continents(ctx):
    start_time = time.time()

    continents = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'], 6: ['6001', '6002', '6003'],
                  8: ['18029', '18030', '18062'], 344:['18303', '18304', '18305']}
    zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir", 344: "Oshur"}
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}
    output = ""

    # servers_data = get_server_data_dummy(servers)
    servers_data = await get_data(servers)
    print("---Requests: %s seconds ---" % (time.time() - start_time))
    print(servers_data)

    #start_time = time.time()

    for server_id in servers_data:
        request = servers_data[server_id]
        for continent in request['map_list']:
            factions = set()
            for region in continent['Regions']['Row']:
                if region['RowData']['RegionId'] in continents[int(continent['ZoneId'])]:
                    factions.add(int(region['RowData']['FactionId']))
            if len(factions) == 3:
                output += "{0}: {1}\n".format(servers[server_id], zones[int(continent['ZoneId'])])

    #print("---Parsing: %s seconds ---" % (time.time() - start_time))

    print(output)
    await ctx.send(output)


bot.run(TOKEN)
