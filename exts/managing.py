import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context


class Manager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    
    @commands.command()
    async def announce(self, ctx: Context, *, message: str):
        pass