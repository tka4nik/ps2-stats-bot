# bot.py
import os
import random

import requests
import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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


@bot.command(name='continents', help='Continents')
async def open_continents(ctx, server_id=None):
    r = requests.get('https://census.daybreakgames.com/s:9641566/get/ps2:v2/character_name/')
    if not (server_id):
        await ctx.send("Emerald: Oshur")
        return
    print(r.text)
    print(r.text)


bot.run(TOKEN)
