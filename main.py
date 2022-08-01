# bot.py
import os

import time
import datetime

import disnake
import requests
from disnake.ext import commands
from dotenv import load_dotenv

import aiohttp
import asyncio

# =======================================# Configuration
load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
bot = commands.InteractionBot(command_prefix='!', intents=disnake.Intents.all(), sync_commands_debug=True,
                              test_guilds=[651509483436113931])
client = disnake.Client()


# =======================================#


# Profiling message on bot connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# Getting all links into 1 array
def get_tasks(session, servers):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8,344".format(SERVICE_ID,
                                                                                                         server_id)
    ) for server_id in servers.keys()]
    return tasks


# Async get data from the servers using event loop
async def get_data(servers):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, servers)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, server_id in zip(responses, servers):
            results[server_id] = await response.json()
        return results


def get_population_tasks(session, servers, url):
    tasks = [session.get(url.format(server_id)) for server_id in servers.keys()]
    return tasks


async def get_population_data(servers, url):
    async with aiohttp.ClientSession() as session:
        tasks = get_population_tasks(session, servers, url)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, server_id in zip(responses, servers):
            results[server_id] = await response.json()
        return results


# Dummy version of the getting data function for testing
def get_server_data_dummy(servers):
    return ""


# Converter of "servers" parameter of "continents" command. Takes a string and returns an id of the server,
# or None if its not a valid server name
def server_to_id_converter(inter, argument):
    servers = {'Emerald': 17, 'Connery': 1, 'Cobalt': 13, 'Miller': 10, 'Soltech': 40}
    if servers.get(argument):
        return servers.get(argument)
    return None


# Parser for the map collection request data
def parser(servers_data, servers, continents, zones):
    output = ""
    for server_id in servers_data:
        request = servers_data[server_id]
        output += "{0}:".format(servers[server_id])
        for continent in request['map_list']:
            factions = set()  # A set to determine if all warpgates have the same faction id (which would mean that the continent is locked)
            for region in continent['Regions']['Row']:
                if region['RowData']['RegionId'] in \
                        continents[
                            int(continent['ZoneId'])]:  # If region_id is in the array of 3 region_ids of warpgates
                    # of the current continent_id
                    factions.add(int(region['RowData']['FactionId']))  # Adding the faction_id to the set
            if len(factions) == 3:
                output += " {0},".format(
                    zones[int(continent['ZoneId'])])  # If there are 3 different factions controlling the warpgates,
                # we are adding the server and continent ot the output
        output = output[:-1:]
        output += "\n"
    return output


# Command that gets open continents for each server
@bot.slash_command(name="continents", description="Open Continents", guild_ids=[651509483436113931])
async def continents(
        inter,
        server: str = commands.Param(
            default=0,
            converter=server_to_id_converter,
            choices={"Emerald": "Emerald",
                     "Connery": "Connery",
                     "Cobalt": "Cobalt",
                     "Miller": "Miller",
                     "Soltech": "Soltech"
                     }
        )):
    await inter.response.defer()  # Request takes too long to respond

    start_time = time.time()  # Timing for testing
    print(server)

    continents = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'],
                  6: ['6001', '6002', '6003'], 8: ['18029', '18030', '18062'],
                  344: ['18303', '18304', '18305']}  # Array of region ids of all warpgates for each continent
    zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir", 344: "Oshur"}  # Array of ids for each zone
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}  # Array of ids for each world

    # Handling the server parameter
    if server:
        tmp = {server: servers[server]}
        servers = tmp

    # servers_data = get_server_data_dummy(servers)
    servers_data = await get_data(servers)  # Getting server data
    print("---Requests: %s seconds ---" % (time.time() - start_time))

    # Parsing
    output = parser(servers_data, servers, continents, zones)

    print(output)
    with open("log/cmd.log", "a+") as f:  # Successful command execution logging
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n" + str(server) + "\n")
        f.write("---Requests: %s seconds ---" % (time.time() - start_time) + "\n")
        f.write(output + "\n")

    await inter.followup.send(output)


@bot.slash_command(name="pop", guild_ids=[651509483436113931])
async def pop(
        inter,
        server: str = commands.Param(
            default=0,
            converter=server_to_id_converter,
            choices={"Emerald": "Emerald",
                     "Connery": "Connery",
                     "Cobalt": "Cobalt",
                     "Miller": "Miller",
                     "Soltech": "Soltech"
                     }
        )):
    await inter.response.defer()
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}
    urls = ["https://ps2.fisu.pw/api/population/?world={0}", "https://wt.honu.pw/api/population/{0}", "https://api.voidwell.com/ps2/worldstate/{0}?platform=pc"]

    if server:
        tmp = {server: servers[server]}
        servers = tmp


    population_data = []
    for url in urls:
        population_data.append(await get_population_data(servers, url))

    ''''
    for server_id in servers.keys():
        res = requests.get("https://ps2.fisu.pw/api/population/?world={0}".format(server_id))
        population_data[server_id] = res.json()['result'][0]['vs'] \
                                     + res.json()['result'][0]['nc'] \
                                     + res.json()['result'][0]['tr'] \
                                     + res.json()['result'][0]['ns']
    '''

    print(population_data)
    #await inter.followup.send(population_data)


@continents.error
async def continents_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that continent...")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Oops, something went wrong...")
    with open("log/err.log", "a+") as f:
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(
            error) + "\n")  # Logging the errors into the error folder


bot.run(TOKEN)
