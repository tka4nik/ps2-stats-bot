import random
import traceback

from logger import GeneralLogger

import discord
from discord.ext import commands


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = GeneralLogger()

    @discord.slash_command(name="twanswate", description="UwU")
    async def twasnwate(self, inter):
        channel = inter.channel
        print((await channel.fetch_message(channel.last_message_id)).content)

        last_message = (await channel.fetch_message(channel.last_message_id))
        print(type(last_message.author.bot))
        print(last_message.author == self.bot)
        if last_message.author.bot:
            await inter.followup.send("Cannot UwU this message")
        else:
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
                name=last_message_content.author.name,
                icon_url=last_message_content.author.avatar.url,
            )
            await inter.response.send_message(embed=embed)

    @twasnwate.error
    async def twanswate_error(self, ctx, error):
        print(error)
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.followup.send("No UwU's above")
        if isinstance(error, discord.ClientException):
            await ctx.followup.send("Cannot UwU bot's message")
        full_error = traceback.format_exception(error)
        self.logger.LogError(str(error) + "\n" + str(full_error), "%d/%m/%y;%H:%M:%S")


def setup(bot):
    bot.add_cog(Other(bot))
