import aiohttp
import asyncio
import disnake
from dotenv import load_dotenv
import os

load_dotenv('settings/.env')
SERVICE_ID = os.getenv('SERVICE_ID')


# Getting all links into 1 array
def get_tasks(session, outfits):
    tasks = [session.get(
        "https://census.daybreakgames.com/s:{0}/get/ps2/outfit?outfit_id={1}&c:show=outfit_id,alias,leader_character_id&c:join=characters_world^on:leader_character_id^to:character_id^inject_at:LeaderWorld^show:world_id".format(
            SERVICE_ID,
            outfit_id)
    ) for outfit_id in outfits.keys()]
    return tasks


# Async get data from the servers using event loop
async def get_data(outfits):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, outfits)
        responses = await asyncio.gather(*tasks)
        results = {}
        for response, outfit in zip(responses, outfits):
            r = await response.json()
            results[outfit] = [r['outfit_list'][0]['alias'], r['outfit_list'][0]['LeaderWorld']['world_id']]
        return results
