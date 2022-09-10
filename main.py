# bot.py
import os
import random

import time
import datetime
from collections import OrderedDict

import auraxium
import discord
from discord import option, commands
import requests
import aiohttp
from discord.ext import tasks

from dotenv import load_dotenv

import websocket
# =======================================#
from population import get_population_data
import continents as cont
import ow_registration
import ow_matchups

# =======================================# Configuration
load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
bot = discord.Bot(debug_guilds=[1005185836201033778], intents=discord.Intents.all())


# =======================================#


# Profiling message on bot connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# Converter of "servers" parameter of "continents" command. Takes a string and returns an id of the server,
# or None if its not a valid server name
def server_to_id_converter(argument):
    servers = {'Emerald': 17, 'Connery': 1, 'Cobalt': 13, 'Miller': 10, 'Soltech': 40}
    if servers.get(argument):
        return servers.get(argument)
    return None


# Command that gets open continents for each server
@bot.slash_command(name="continents", description="Open Continents")
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
async def continents(inter, server: str):
    await inter.response.defer()  # Request takes too long to respond

    start_time = time.time()  # Timing for testing
    print(server)
    server = server_to_id_converter(server)

    continents_list = {2: ['2201', '2202', '2203'], 4: ['4230', '4240', '4250'],
                       6: ['6001', '6002', '6003'], 8: ['18029', '18030', '18062'],
                       344: ['18303', '18304', '18305']}  # Array of region ids of all warpgates for each continent
    zones = {2: 'Indar', 4: "Hossin", 6: "Amerish", 8: "Esamir", 344: "Oshur"}  # Array of ids for each zone
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}  # Array of ids for each world

    # Handling the server parameter
    if server:
        tmp = {server: servers[server]}
        servers = tmp

    # servers_data = get_server_data_dummy(servers)
    servers_data = await cont.get_data(servers)  # Getting server data
    print(servers_data)
    population_data = await get_population_data(server, servers)
    print("---Requests: %s seconds ---" % (time.time() - start_time))

    # Parsing
    output = cont.parser(servers_data, servers, continents_list, zones, population_data)

    print(output)
    with open("log/cmd.log", "a+") as f:  # Successful command execution logging
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n" + str(server) + "\n")
        f.write("---Requests: %s seconds ---" % (time.time() - start_time) + "\n")
        f.write(output + "\n")

    await inter.followup.send(output)


@continents.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    print(error)
    if isinstance(error, discord.InvalidArgument):
        await ctx.followup.send("I could not find that continent...")
    if isinstance(error, discord.ApplicationCommandInvokeError):
        await ctx.followup.send("Oops, something went wrong...")
    with open("log/err.log", "a+") as f:
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(
            error) + "\n")  # Logging the errors into the error folder


# UwU
@bot.slash_command(name="twanswate", description="UwU")
async def twasnwate(inter):
    channel = bot.get_channel(1005185837060849720)
    print((await channel.fetch_message(channel.last_message_id)).content)
    last_message = (await channel.fetch_message(channel.last_message_id))

    last_message_content = last_message.content

    letters = "aeyuio ,.;@#$%^&*()_-=+][{}|\\\"\'"
    for i in range(len(last_message_content)):
        if last_message_content[i] not in letters:
            if random.random() > 0.8:
                last_message_content = last_message_content[:i] + "w" + last_message_content[i + 1:]
                i += 1
    print(last_message_content)
    embed = discord.Embed(
        title="",
        description=last_message_content,
        colour=0xF0C43F,
    )
    embed.set_author(
        name=last_message.author.name,
        icon_url=last_message.author.avatar.url,
    )

    await inter.response.send_message(embed=embed)


@twasnwate.error
async def twanswate_error(ctx, error):
    if isinstance(error, discord.ApplicationCommandInvokeError):
        await ctx.send("No UwU's above")
    with open("log/err.log", "a+") as f:
        f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + str(
            error) + "\n")  # Logging the errors into the error folder


# Command that get the list of registered OW outfits
@bot.slash_command(name="ow")
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
async def ow(inter, server: str):
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

    if output:
        embed = discord.Embed(
            title="",
            description=output,
            colour=0xF0C43F,
        )
        await inter.followup.send(embed=embed)
    else:
        await inter.followup.send("No data found")


@bot.slash_command(name="matchups")
async def matchaps(inter):
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
    await inter.followup.send(output)


@tasks.loop(count=1)
async def census_watchtower():
    await item_added_updater()


async def item_added_updater():
    print("doing stuff")
    client = auraxium.event.EventClient(service_id="s:" + str(SERVICE_ID))

    channel = bot.get_channel(1018207605308543116)

    @client.trigger(auraxium.event.ItemAdded, worlds=[13])
    async def itemadded_action(event):
        if event.context == "GuildBankWithdrawal":
            char_id = event.character_id
            character_outfit_data = requests.get(
                "https://census.daybreakgames.com/s:{0}/get/ps2:v2/outfit_member?character_id={1}&c:join=outfit^show:alias&c:join=character^show:name".format(
                    SERVICE_ID, char_id)).json()["outfit_member_list"][0]

            if character_outfit_data["outfit_id_join_outfit"]["alias"] == "H":
                item_name = requests.get(
                    "https://census.daybreakgames.com/s:{0}/get/ps2:v2/item?item_id={1}&c:show=name".format(SERVICE_ID, event.item_id)).json()["item_list"][0]["name"]["en"]
                output = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S") + ";item_name" + ";" + character_outfit_data["outfit_id_join_outfit"]["alias"] + ";" + character_outfit_data["character_id_join_character"]["name"]["first"]
                discord_output = datetime.datetime.now().strftime("%H:%M") + "; " + item_name + "; called by " + character_outfit_data["character_id_join_character"]["name"]["first"]
                print(output)

                await channel.send(discord_output)

                log_output(output, "log/ws.log", "%d/%m/%y %H:%M:%S")

            if character_outfit_data["outfit_id_join_outfit"]["alias"] == "RMIS":
                item_name = requests.get(
                    "https://census.daybreakgames.com/s:{0}/get/ps2:v2/item?item_id={1}&c:show=name".format(SERVICE_ID,
                                                                                                            event.item_id)).json()[
                    "item_list"][0]["name"]["en"]
                print(character_outfit_data)
                output = ";" + item_name + ";" + character_outfit_data["outfit_id_join_outfit"]["alias"] + ";" + character_outfit_data["character_id_join_character"]["name"]["first"]
                discord_output = datetime.datetime.now().strftime("%H:%M") + "; " + item_name + "; called by " + character_outfit_data["character_id_join_character"]["name"]["first"]
                print(output)
                log_output(output, "log/ws.log", "%d/%m/%y;%H:%M:%S")


def log_output(output, file, format):
    with open(file, "a+") as f:
        f.write(datetime.datetime.now().strftime(format) + str(output) + "\n")


@bot.slash_command(name="websocket_start")
async def websocket_start(inter):
    print(inter)
    census_watchtower.start()
    await inter.response.send_message("Websocket is running!")


@bot.slash_command(name="websocket_stop")
async def websocket_stop(inter):
    census_watchtower.stop()
    await inter.response.send_message("Websocket is stopped!")


bot.run(TOKEN)
