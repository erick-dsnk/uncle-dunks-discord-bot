import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Context, MissingPermissions
from discord.utils import get


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: discord.Member, *, reason="None specified."):
        dm_chnl = await member.create_dm()

        chnl = ctx.channel

        server = ctx.guild.name

        await dm_chnl.send(f"The staff have decided to kick you from {server} for reason: {reason}")
        await member.kick(reason=reason)

        await chnl.send(f":white_check_mark: Kicked user {member.name}#{member.discriminator} for reason: {reason}. Also logged incident, to see previous incidents in this server, type `-incidents` (WIP)")

    @kick.error
    async def kick_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: You don't have permission to use this command")


    # Ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: discord.Member, *, reason="None specified."):
        dm_chnl = await member.create_dm()

        chnl = ctx.channel

        server = ctx.guild.name
        server_id = ctx.guild.id

        await dm_chnl.send(f"The staff have decided to ban you from {server} for reason: {reason}")
        await member.ban(reason=reason)

        await chnl.send(f":white_check_mark: Successfully banned user {member.mention} for reason: {reason}")
    
    @ban.error
    async def ban_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: You don't have permission to use this command")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def mute(self, ctx: Context, user: discord.Member, duration: str = "15m"):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.send_messages = False
            await channel.set_permissions(user, overwrite=perms, reason="mute")

        await ctx.send(f":white_check_mark: Successfully muted {user.mention} for `{duration}`!")

        if 's' in duration:
            duration = int(duration.strip('s'))
        
        elif 'm' in duration:
            duration = int(duration.strip('m')) * 60
        
        elif 'h' in duration:
            duration = int(duration.strip('h')) * 3600
        
        elif 'd' in duration:
            duration = int(duration.strip('d')) * 86400
        
        else:
            duration = int(duration)

        await asyncio.sleep(duration)

        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.send_messages = True
            await channel.set_permissions(user, overwrite=perms, reason="unmute")

        await ctx.send(f":white_check_mark: Successfully unmuted {user.mention}!")

    @mute.error
    async def mute_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f":x: You don't have permission to use that command! {ctx.message.author.mention}")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def unmute(self, ctx: Context, user: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.send_messages = True
            await channel.set_permissions(user, overwrite=perms, reason="unmute")

        await ctx.send(f":white_check_mark: Successfully unmuted {user.mention}!")

    @unmute.error
    async def unmute_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f":x: You don't have permission to use that command! {ctx.message.author.mention}")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def vcmute(self, ctx: Context, user: discord.Member, duration: str = '15m'):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.speak = False
            await channel.set_permissions(user, overwrite=perms, reason="vc mute")

        await ctx.send(f":white_check_mark: Successfully muted {user.mention} for `{duration}`!")

        if 's' in duration:
            duration = int(duration.strip('s'))

        elif 'm' in duration:
            duration = int(duration.strip('m')) * 60

        elif 'h' in duration:
            duration = int(duration.strip('h')) * 3600

        elif 'd' in duration:
            duration = int(duration.strip('d')) * 86400

        else:
            duration = int(duration)

        await asyncio.sleep(duration)

        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.speak = True
            await channel.set_permissions(user, overwrite=perms, reason="vc unmute")

        await ctx.send(f":white_check_mark: Successfully unmuted {user.mention}!")


    @vcmute.error
    async def vcmute_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f":x: You don't have permission to use that command! {ctx.message.author.mention}")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def vcunmute(self, ctx: Context, user: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.speak = True
            await channel.set_permissions(user, overwrite=perms, reason="vc unmute")

        await ctx.send(f":white_check_mark: Successfully unmuted {user.mention}!")
    
    @vcunmute.error
    async def vcunmute_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f":x: You don't have permission to use that command! {ctx.message.author.mention}")


def setup(bot):
    bot.add_cog(Moderation(bot))
