import discord
from discord.ext import commands
from datetime import datetime
from discord.utils import get


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="None specified."):
        dm_chnl = await member.create_dm()

        chnl = ctx.channel

        server = ctx.guild.name

        try:
            await dm_chnl.send(f"The staff have decided to kick you from {server} for reason: {reason}")
            await member.kick(reason=reason)

            await chnl.send(f":white_check_mark: Kicked user {member.name}#{member.discriminator} for reason: {reason}. Also logged incident, to see previous incidents in this server, type `-incidents` (WIP)")

        except Exception as e:
            print(e)

            await chnl.send(f":x: Couldn't kick user {member}.")


    # Ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="None specified."):
        dm_chnl = await member.create_dm()

        chnl = ctx.channel

        server = ctx.guild.name
        server_id = ctx.guild.id

        try:
            await dm_chnl.send(f"The staff have decided to ban you from {server} for reason: {reason}")
            await member.ban(reason=reason)

            await chnl.send(f":white_check_mark: Banned user {member.name}#{member.discriminator} for reason: {reason}. Also logged incident, to see previous logs in this server, type `-incidents` (WIP)")

        except Exception as e:
            print(e)

            await chnl.send(f":x: Couldn't ban user {member}.")


def setup(bot):
    bot.add_cog(Moderation(bot))