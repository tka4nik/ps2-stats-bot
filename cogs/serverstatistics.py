import time
import datetime
import traceback

from . import continents as cont
from .population import get_population_data
from logger import GeneralLogger

import auraxium
import discord
from discord import option
from discord.ext import commands
import requests
import aiohttp
from discord.ext import tasks
from dotenv import load_dotenv
import os


SERVICE_ID = os.getenv('SERVICE_ID')
print("serverstatistics " + str(SERVICE_ID))


class ServerStatistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = GeneralLogger()

    @discord.slash_command(name="continents", description="Open Continents")
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
    async def continents(self, inter, server: str):
        await inter.response.defer()  # Request takes too long to respond

        start_time = time.time()  # Timing for testing
        print(server)
        server = server_to_id_converter(server)

        continents_list = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'],
                           6: ['6001', '6002', '6003'], 8: ['18029', '18030', '18062'],
                           344: ['18303', '18304', '18305']}  # Array of region ids of all warpgates for each continent
        zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir", 344: "Oshur"}  # Array of ids for each zone
        servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller',
                   40: 'Soltech'}  # Array of ids for each world

        # Handling the server parameter
        if server:
            tmp = {server: servers[server]}
            servers = tmp

        # servers_data = get_server_data_dummy(servers)
        servers_data = await cont.get_data(servers)  # Getting server data
        print(servers_data)
        population_data = await get_population_data(server, servers)

        # Parsing
        output = cont.parser(servers_data, servers, continents_list, zones, population_data)

        print(output)
        self.logger.LogCommand(output, "%d/%m/%y;%H:%M:%S")

        await inter.followup.send(output)

    @continents.error
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        print(error)
        if isinstance(error, discord.InvalidArgument):
            await ctx.followup.send("I could not find that continent...")
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.followup.send("Oops, something went wrong...")
        full_error = traceback.format_exception(error)
        self.logger.LogError(str(error) + "\n" + str(full_error), "%d/%m/%y;%H:%M:%S")


def setup(bot):
    bot.add_cog(ServerStatistics(bot))


# Converter of "servers" parameter of "continents" command. Takes a string and returns an id of the server,
# or None if its not a valid server name
def server_to_id_converter(argument):
    servers = {'Emerald': 17, 'Connery': 1, 'Cobalt': 13, 'Miller': 10, 'Soltech': 40}
    if servers.get(argument):
        return servers.get(argument)
    return None
