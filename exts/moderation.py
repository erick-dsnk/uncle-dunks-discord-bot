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
        '''
        Kick a member from the server.
        Usage: `-kick @BadCookie#0001 You are a bad cookie >:(`
        '''
        
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
        '''
        Ban a member from the server.
        Usage: `-ban @BadCookie#0001 You are a VERY bad cookie >:(`
        '''
        
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
        '''
        Restrict a member from sending messages
        Duration is an optional argument and it will mute the member for 15 minutes if none is given.
        The duration argument can be passed in seconds (`50s`), minutes (`20m`), hours (`2h`) or days (`7d`).
        '''
        
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
        '''
        It gives the member ability to send messages again.
        '''

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
        '''
        Restrict a member speaking in voice channels
        Duration is an optional argument and it will mute the member for 15 minutes if none is given.
        The duration argument can be passed in seconds (`50s`), minutes (`20m`), hours (`2h`) or days (`7d`).
        '''
        
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
        '''
        It gives the member ability to speak in voice channels again.
        '''
        
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(user)
            perms.speak = True
            await channel.set_permissions(user, overwrite=perms, reason="vc unmute")

        await ctx.send(f":white_check_mark: Successfully unmuted {user.mention}!")
    
    @vcunmute.error
    async def vcunmute_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f":x: You don't have permission to use that command! {ctx.message.author.mention}")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def silence(self, ctx: Context, duration: str = "15m"):
        '''
        It mutes every person in the channel to give moderators time to intervene and handle the situation.
        '''
        initial_duration = duration
        
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
        

        channel = ctx.channel

        for member in channel.members:
            perms = channel.overwrites_for(member)
            perms.send_messages = False
            await channel.set_permissions(member, overwrite=perms, reason="silence")

        await ctx.send(f":white_check_mark: Channel has been silenced for `{initial_duration}`.")

        await asyncio.sleep(duration)

        for member in channel.members:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms, reason="unsilence")

        await ctx.send(":white_check_mark: Channel has been unsilenced.")


    @silence.error
    async def silence_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You're not allowed to use that command!")


    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def unsilence(self, ctx: Context):
        '''
        Give back members of the channel the permission to chat again.
        '''
        channel = ctx.channel

        for member in channel.members:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms, reason="unsilence")

        await ctx.send(":white_check_mark: Channel has been unsilenced.")


    @unsilence.error
    async def unsilence_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You're not allowed to use that command!")


def setup(bot):
    bot.add_cog(Moderation(bot))
