import discord
from discord.ext import commands
from datetime import datetime
from helpers.incident_tracker import log_incident, retrieve_incidents
from discord.utils import get


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # Command that silences every channel in case of a raid and gives staff time to react
    @commands.command(aliases=['s'])
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def silence(self, ctx, reason="None specified."):
        members = ctx.guild.members

        silenced_role = get(ctx.guild.roles, name='Silenced')

        server = ctx.guild.id

        for member in members:
            await member.add_roles(silenced_role)
        
        chnl = ctx.channel

        await chnl.send(":white_check_mark: I silenced all the channels to give the staff time to react to this issue.")

        log_incident("silence-channels", reason, f"{datetime.day}.{datetime.month}.{datetime.year} at {datetime.time}", server)



    # Command that unsilences all the channels after the staff handled the issues
    @commands.command(aliases=['us'])
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def unsilence(self, ctx):
        silenced_role = get(ctx.guild.roles, name='Silenced')

        members = silenced_role.members

        for member in members:
            await member.remove_roles(silenced_role)
        
        chnl = ctx.channel
        
        await chnl.send(":white_check_mark: Unsilenced all channels.")


    # Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="None specified."):
        dm_chnl = await member.create_dm()

        chnl = ctx.channel

        server = ctx.guild.name
        server_id = ctx.guild.id

        try:
            await dm_chnl.send(f"The staff have decided to kick you from {server} for reason: {reason}")
            await member.kick(reason=reason)

            log_incident('ban_member', reason, f"{datetime.day()}.{datetime.month()}.{datetime.year()} at {datetime.time()}", server_id)

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

            log_incident('ban_member', reason, f"{datetime.day()}.{datetime.month()}.{datetime.year()} at {datetime.time()}", server_id)

            await chnl.send(f":white_check_mark: Banned user {member.name}#{member.discriminator} for reason: {reason}. Also logged incident, to see previous logs in this server, type `-incidents` (WIP)")

        except Exception as e:
            print(e)

            await chnl.send(f":x: Couldn't ban user {member}.")


    # Show all incidents in that server command
    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def incidents(self, ctx):
        _incidents = retrieve_incidents(ctx.guild.id)

        chnl = ctx.channel

        if _incidents != None:

            iterations = 0

            if len(_incidents) > 30:
                iterations = 30
            else:
                iterations = len(_incidents)

            for i in range(iterations):
                await chnl.send(f"Incident: {_incidents[i]['incident']}\nReason: {_incidents[i]['reason']}\nDate and time: {_incidents[i]['time']}")

        else:
            await chnl.send(":white_check_mark: I couldn't find any incidents, good job on managing this server so well!")


def setup(bot):
    bot.add_cog(Moderation(bot))