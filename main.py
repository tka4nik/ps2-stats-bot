# bot.py
import os

import random
import time
import datetime

import discord
from dotenv import load_dotenv
from discord.ext import commands

import aiohttp
import asyncio

# =======================================
# Configuration
load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')
intents = discord.Intents.default()  # Gets the default intents from discord.
intents.members = True  # Enables members intents on the bot.
bot = commands.Bot(command_prefix='!', intents=intents)  # Applies those intents


# =======================================


# Profiling message on bot connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# Errors handler
@bot.event
async def on_command_error(ctx, error):
    print(error)
    print(ctx.command)
    print(discord.HTTPException)
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):  # Command not found error handler
        await ctx.send('Command not found!')
    if isinstance(error, discord.ext.commands.CommandInvokeError):
        if "400" in str(error):
            await ctx.send(
                'No continents are open at the moment/the servers are down!')  # If the error message contains code 400, that means the message was empty or the servers are down
        else:
            await ctx.send('Something wrong has happened!')
    with open("log/err.log", "a+") as f:
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(
            error) + "\n")  # Logging the errors into the error folder


# =======================================
# Async version of getting 5 queries from map collection
# =======================================

# Getting all links in 1 array
def get_tasks(session, servers):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8,344".format(SERVICE_ID,
                                                                                                         server_id)) for
        server_id in servers.keys()]
    return tasks


# async get data from the servers using event loop
async def get_data(servers):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, servers)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, server_id in zip(responses, servers):
            results[server_id] = await response.json()
        return results


# Dummy version of the getting data function for testing
def get_server_data_dummy(servers):
    return ""


# =======================================
# Command that gets open continents for each server
@bot.command(name='c', help='Open continents')
async def open_continents(ctx):
    start_time = time.time()  # Timing for testing

    continents = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'], 6: ['6001', '6002', '6003'],
                  8: ['18029', '18030', '18062'],
                  344: ['18303', '18304', '18305']}  # Array of region ids of all warpgates for each continent
    zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir", 344: "Oshur"}  # Array of ids for each zone
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}  # Array of ids for each world
    output = ""

    # servers_data = get_server_data_dummy(servers)
    servers_data = await get_data(servers)  # Getting server data
    print("---Requests: %s seconds ---" % (time.time() - start_time))
    print(servers_data)

    # start_time = time.time()
    # Parsing # =======================================
    for server_id in servers_data:
        request = servers_data[server_id]
        for continent in request['map_list']:
            factions = set()  # A set to determine if all warpgates have the same faction id (which would mean that the continent is locked)
            for region in continent['Regions']['Row']:
                if region['RowData']['RegionId'] in continents[int(continent[
                                                                       'ZoneId'])]:  # If region_id is in the array of 3 region_ids of warpgates of the current continent_id
                    factions.add(int(region['RowData']['FactionId']))  # Adding the faction_id to the set
            if len(factions) == 3:
                output += "{0}: {1}\n".format(servers[server_id], zones[int(continent[
                                                                                'ZoneId'])])  # If there are 3 different factions controlling the warpgates, we are adding the server and continent ot the output

    # print("---Parsing: %s seconds ---" % (time.time() - start_time))

    print(output)
    await ctx.send(output)


bot.run(TOKEN)
