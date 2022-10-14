import aiohttp
import asyncio
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
SERVICE_ID = os.getenv('SERVICE_ID')
print(SERVICE_ID)


# Getting all links into 1 array
def get_tasks(session, outfits):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2/outfit?outfit_id={1}&c:show=alias".format(
            SERVICE_ID,
            outfit_id)
    ) for outfit_id in outfits]
    return tasks


# Async get data from the servers using event loop
async def get_data(outfits):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, outfits)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, outfit in zip(responses, outfits):
            r = await response.json()
            results[outfit] = r['outfit_list'][0]['alias']
        return results


# Parser (`rank: alias, faction`)
def parser(data_dict_sorted):
    output = ""
    factions = {1: "<:vs:441405448113881098>", 2: "<:nc:441405432091901972>", 3: "<:tr:441405413745754112>"}
    print(data_dict_sorted[2][0])
    print(factions[data_dict_sorted[2][1]])
    for i in range(10, 0, -1):
        if i % 2 != 0:
            output += "\t" + "vs.\t"
        output += factions[data_dict_sorted[i][1]] + " " + data_dict_sorted[i][0]
        if i % 2 != 0:
            output += "\n"
    return output