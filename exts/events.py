import discord
from discord import Game
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Uncle Dunk\'s bot is in the house and he ain\'t leaving')
        await self.bot.change_presence(status=discord.Status.dnd, activity=Game(name="||| -help to see a list of commands! |||"))


def setup(bot):
    bot.add_cog(Events(bot))