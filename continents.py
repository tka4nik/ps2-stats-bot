import aiohttp
import asyncio
import disnake
from dotenv import load_dotenv
import os

load_dotenv('settings/.env')
SERVICE_ID = os.getenv('SERVICE_ID')


# Getting all links into 1 array
def get_tasks(session, servers):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8,344".format(
            SERVICE_ID,
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


# Dummy version of the getting data function for testing
def get_server_data_dummy(servers):
    return ""


# Parser for the map collection request data
def parser(servers_data, servers, continents, zones, population_data):
    output = ""
    for server_id in servers_data:
        request = servers_data[server_id]
        output += "**{0}**:".format(servers[server_id])
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
        output += ";\nOnline: {0}".format(population_data[server_id])
        output += "\n"
    return output
