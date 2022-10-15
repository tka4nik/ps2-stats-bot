import time
import datetime

from . import ow_registration
from . import ow_matchups
from . import war_assets
from logger import GeneralLogger

import auraxium
import discord
from discord import option
from discord.ext import commands
import requests
import aiohttp
from discord.ext import tasks
import os

SERVICE_ID = os.getenv('SERVICE_ID')
print("outfitwars " + str(SERVICE_ID))


class OutfitWars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = GeneralLogger()

    @discord.slash_command(name="ow")
    @option(
        "server",
        description="Pick a server",
        required=False,
        default='',
        choices={"Emerald": "Emerald",
                 "Connery": "Connery",
                 "Cobalt": "Cobalt",
                 "Miller": "Miller",
                 "Soltech": "Soltech"
                 },
    )
    async def ow(self, inter, server: str):
        await inter.response.defer()  # Request takes too long to respond
        server = server_to_id_converter(server)

        ow_reg = requests.get(
            "https://census.lithafalcon.cc/get/ps2/outfit_war_registration?c:limit=1000").json()  # Getting the list of signups from Falcon's API
        outfit_id_dic = {}
        outfit_id_world_dic = {}

        for outfit in ow_reg[
            'outfit_war_registration_list']:  # Creates a dictionary of `outfit_id: registered members count`
            outfit_id_dic[outfit['outfit_id']] = [outfit['member_signup_count'], outfit['status']]
            print(outfit['outfit_id'], outfit['member_signup_count'])
        print(outfit_id_dic)

        outfits_list = await ow_registration.get_data(outfit_id_dic)  # Gets a dictionary of `outfit_id: [tag, count]`
        print(outfits_list)

        output = ow_registration.parser(outfit_id_dic, outfits_list, server)  # Parser

        self.logger.LogCommand(output, "%d/%m/%y;%H:%M:%S")

        if output:
            embed = discord.Embed(
                title="",
                description=output,
                colour=0xF0C43F,
            )
            await inter.followup.send(embed=embed)
        else:
            await inter.followup.send("No data found")

    @discord.slash_command(name="matchups")
    async def matchups(self, inter):
        await inter.response.defer()
        print(time.time())
        data = requests.get(
            "https://census.lithafalcon.cc/get/ps2/outfit_war_match?world_id=13&c:hide=match_id,outfit_war_id,world_id&c:sort=order&start_time=%3E{0}"
                .format(round(time.time()))).json()['outfit_war_match_list']
        print(data)

        outfits = []
        for item in data:
            outfits.append(item['outfit_a_id'])
            outfits.append(item['outfit_b_id'])
        outfits_aliases = []
        try:
            outfits_aliases = await ow_matchups.get_data(outfits)  # Get aliases for each outfit id
        except aiohttp.ClientOSError as e:
            inter.followup.send("Something is wrong..")
            with open("log/err.log", "a+") as f:
                f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(
                    e) + "\n")  # Logging the errors into the error folder
        print(outfits_aliases)

        output = ""
        factions = {1: "<:vs:441405448113881098>", 2: "<:nc:441405432091901972>", 3: "<:tr:441405413745754112>"}

        for item in data:
            output += factions[int(item['outfit_a_faction_id'])] + " " + outfits_aliases[item['outfit_a_id']]
            output += "\t vs. \t"
            output += factions[int(item['outfit_b_faction_id'])] + " " + outfits_aliases[item['outfit_b_id']]
            output += ":  --  at a time:  `" + str(
                time.strftime("%a, %d %b %Y %H:%M", time.gmtime(int(item['start_time'])))) + "`"
            print(time.strftime("%a, %d %b %Y %H:%M", time.gmtime(int(item['start_time']))))
            output += "\n"

        print(output)
        self.logger.LogCommand(output, "%d/%m/%y;%H:%M:%S")
        await inter.followup.send(output)

    @commands.Cog.listener()
    async def census_watchtower(self):
        await war_assets.item_added_updater(self.bot)

    @discord.slash_command(name="websocket_start")
    async def websocket_start(self, inter):
        print(inter)
        await self.census_watchtower()
        await inter.response.send_message("Websocket is running!")


def setup(bot):
    bot.add_cog(OutfitWars(bot))


# Converter of "servers" parameter of "continents" command. Takes a string and returns an id of the server,
# or None if its not a valid server name
def server_to_id_converter(argument):
    servers = {'Emerald': 17, 'Connery': 1, 'Cobalt': 13, 'Miller': 10, 'Soltech': 40}
    if servers.get(argument):
        return servers.get(argument)
    return None


