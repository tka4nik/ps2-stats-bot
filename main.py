# bot.py
import os
import discord
from dotenv import load_dotenv

# =======================================# Configuration
load_dotenv('settings/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
SERVICE_ID = os.getenv('SERVICE_ID')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
bot = discord.Bot(debug_guilds=[1005185836201033778, 784850292981366844], intents=discord.Intents.all())
cog_list = [
    'outfitwars',
    'serverstatistics',
    'other'
]
# =======================================#

for cog in cog_list:
    bot.load_extension(f'cogs.{cog}')


# Profiling message on bot connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
