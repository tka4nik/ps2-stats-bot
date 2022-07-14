# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default() # Gets the default intents from discord.
intents.members = True # enables members intents on the bot.

client = discord.Client(intents=intents)


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
