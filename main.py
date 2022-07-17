# bot.py
import os
import random
import pprint

import requests
import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')

intents = discord.Intents.default()  # Gets the default intents from discord.
intents.members = True  # enables members intents on the bot.

'''client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(
        f'{client.user} has connected to Discord!\n'
    )

@client.event
async def on_member_join(member):
    print(member)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("The message's content was", message.content, message.author.name)

    if message.content == '!alerts':
        response = "Fuck you"
        await message.channel.send(response)

client.run(TOKEN)
'''
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='99', help='Random quote')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='c', help='Open continents')
async def open_continents(ctx, server=None):
    indar_wg = ['2201', '2202', '2203']
    hossin_wg = ['4230', '4240', '4250']
    amerish_wg = ['6001', '6002', '6003']
    esamir_wg = ['18029', '18030', '18062']
    servers = {17: 'Emerald', 1: 'Connery', 13: 'Cobalt', 10: 'Miller', 40: 'Soltech'}
    for server_id in servers.keys():
        r = requests.get('https://census.daybreakgames.com/s:{0}/get/ps2:v2/map?world_id={1}&zone_ids=2,4,6,8'.format(SERVICE_ID, server_id))
        request = r.json()
        indar = set()
        esamir = set()
        amerish = set()
        hossin = set()
        for continent in request['map_list']:
            for region in continent['Regions']['Row']:
                if region['RowData']['RegionId'] in indar_wg:
                    indar.add(int(region['RowData']['FactionId']))
                if region['RowData']['RegionId'] in hossin_wg:
                    hossin.add(region['RowData']['FactionId'])
                if region['RowData']['RegionId'] in amerish_wg:
                    amerish.add(region['RowData']['FactionId'])
                if region['RowData']['RegionId'] in esamir_wg:
                    esamir.add(region['RowData']['FactionId'])
        if len(indar) == 3:
            print("{0}: Indar".format(servers[server_id]))
            await ctx.send("{0}: Indar".format(servers[server_id]))
        if len(esamir) == 3:
            print("{0}: Esamir".format(servers[server_id]))
            await ctx.send("{0}: Esamir".format(servers[server_id]))
        if len(amerish) == 3:
            print("{0}: Amerish".format(servers[server_id]))
            await ctx.send("{0}: Amerish".format(servers[server_id]))
        if len(hossin) == 3:
            print("{0}: Hossin".format(servers[server_id]))
            await ctx.send("{0}: Hossin".format(servers[server_id]))

bot.run(TOKEN)
