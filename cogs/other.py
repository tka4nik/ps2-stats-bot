import random
import time
import datetime

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


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = GeneralLogger()

    @discord.slash_command(name="twanswate", description="UwU")
    async def twasnwate(self, inter):
        channel = self.bot.get_channel(1005185837060849720)
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
        self.logger.LogCommand(last_message_content, "%d/%m/%y;%H:%M:%S")
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
    async def twanswate_error(self, ctx, error):
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.send("No UwU's above")
        self.logger.LogError(error, "%d/%m/%y;%H:%M:%S")

def setup(bot):
    bot.add_cog(Other(bot))