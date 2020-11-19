import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot


class Economy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Economy(bot))