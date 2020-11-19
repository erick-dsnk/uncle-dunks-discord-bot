import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context


class Gambling(Cog):
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Gambling(bot))