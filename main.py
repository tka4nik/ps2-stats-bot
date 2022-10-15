# bot.py
import os
import random

import time
import datetime

import discord
from discord import option

from dotenv import load_dotenv

# =======================================#
from cogs.population import get_population_data
from cogs import continents as cont

# =======================================# Configuration
load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
bot = discord.Bot(debug_guilds=[1005185836201033778, 784850292981366844], intents=discord.Intents.all())

# =======================================#

cog_list = [
    'outfitwars',
    'serverstatistics'
]

for cog in cog_list:
    bot.load_extension(f'cogs.{cog}')

# Profiling message on bot connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
