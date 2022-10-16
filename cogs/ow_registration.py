import aiohttp
import asyncio
import os

SERVICE_ID = os.getenv('SERVICE_ID')
print("ow_registration " + str(SERVICE_ID))


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


# Parser for the latest outfit dictionary (id: tag, count)
def parser(outfit_id_dic, outfits_list, server):
    output = ""
    for outfit in outfit_id_dic:
        if server:
            if int(outfits_list[outfit][1]) == server:
                if outfit_id_dic[outfit][1] == "Full":
                    output += "**" + str(outfits_list[outfit][0]) + ": " + str(outfit_id_dic[outfit][0]) + "**"
                    output += '\n'
                else:
                    output += str(outfits_list[outfit][0]) + ": " + str(outfit_id_dic[outfit][0])
                    output += '\n'
        else:
            if outfit_id_dic[outfit][1] == "Full":
                output += "**" + str(outfits_list[outfit][0]) + ": " + str(outfit_id_dic[outfit][0]) + "**"
                output += '\n'
            else:
                output += str(outfits_list[outfit][0]) + ": " + str(outfit_id_dic[outfit][0])
                output += '\n'
    return output
