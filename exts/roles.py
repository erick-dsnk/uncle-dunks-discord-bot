import discord
from discord import Role
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot


class Roles(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    

    @commands.command(aliases=['ar'])
    def addrole(self, ctx: Context, role) -> None:
        if type(role) == str:
            pass

        elif type(role) == int:
            pass

        elif type(role) == Role:
            pass