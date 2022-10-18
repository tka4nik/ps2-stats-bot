import os
import time
import traceback

import discord
from discord import option
from discord.ext import commands

from . import continents as cont
from .population import get_population_data
from logger import GeneralLogger
import config


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
        servers = config.servers
        start_time = time.time()  # Timing for testing
        server = server_to_id_converter(server)

        # Handling the server parameter
        if server:
            tmp = {server: config.servers[server]}
            servers = tmp

        # servers_data = get_server_data_dummy(servers)
        servers_data = await cont.get_data(servers)  # Getting server data
        population_data = await get_population_data(server, servers)

        # Parsing
        output = cont.parser(servers_data, servers, config.continents_list, config.zones, population_data)

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
