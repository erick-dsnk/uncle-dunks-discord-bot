from datetime import datetime
import inspect
from typing import Tuple
import discord
from discord import Role
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from discord.utils import get

class Roles(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    

    @commands.has_permissions(manage_roles=True)
    @commands.command(aliases=['ar'])
    async def addrole(self, ctx: Context, member: discord.Member, role) -> None:
        '''
        Add a role to a user!
        Role can be in the form of an ID, name, or a role mention!
        '''
        try:
            role = int(role)

        except Exception as e:
            pass


        if type(role) == str:
            for r in ctx.guild.roles:
                if role.lower() in r.name.lower():
                    await member.add_roles(r)

                    embed = discord.Embed(
                        title=":white_check_mark: Success!",
                        description=f"Added role `{r.name}` to {member.mention}!",
                        color=discord.Color.green()
                    )

                    await ctx.send(embed=embed)

            else:
                await ctx.send(":x: Couldn't find a role with that name!")

        elif type(role) == int:
            r = get(ctx.guild.roles, id=role)

            if r:
                await member.add_roles(r)

                embed = discord.Embed(
                    title=":white_check_mark: Success!",
                    description=f"Added role to {member.mention}!",
                    color=discord.Color.green()
                )

                await ctx.send(embed=embed)
            
            else:
                await ctx.send(":x: Couldn't find a role with that ID!")

    

    @commands.has_permissions(manage_roles=True)
    @commands.command(aliases=['rr'])
    async def removerole(self, ctx: Context, member: discord.Member, role) -> None:
        '''
        Remove a role from a user!
        Role can be in the form of an ID, name, or a role mention!
        '''
        try:
            role = int(role)

        except Exception as e:
            pass


        if type(role) == str:
            for r in ctx.guild.roles:
                if role.lower() in r.name.lower():
                    await member.remove_roles(r)

                    embed = discord.Embed(
                        title=":white_check_mark: Success!",
                        description=f"Removed role `{r.name}` from {member.mention}!",
                        color=discord.Color.green()
                    )

                    await ctx.send(embed=embed)
            
            else:
                await ctx.send("Couldn't find a role with that name!")


        elif type(role) == int:
            r = get(ctx.guild.roles, id=role)

            if r:
                await member.remove_roles(r)

                embed = discord.Embed(
                    title=":white_check_mark: Success!",
                    description=f"Removed role `{r.name}` from {member.mention}!",
                    color=discord.Color.green()
                )

                await ctx.send(embed=embed)

            else:
                await ctx.send(":x: Couldn't find a role with that ID!")


    @commands.command()
    async def roleinfo(self, ctx: Context, role):
        '''
        Get information about a role!
        '''

        try:
            role = int(role)

        except Exception as e:
            pass
    
        if type(role) == int:
            role = get(ctx.guild.roles, id=int(role))

            if not role:
                await ctx.send(":x: Couldn't find a role with that ID!")
                return

        
        elif type(role) == str:
            for r in ctx.guild.roles:
                if role.lower() in r.name.lower():
                    role = r
                
            else:
                await ctx.send(":x: Couldn't find a role with that name!")
                return

        embed = discord.Embed(
            title="Role Info",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Name",
            value=f"`{role.name}`",
            inline=True
        )

        embed.add_field(
            name="Role Color",
            value=f"`{role.color}`",
            inline=True
        )

        embed.add_field(
            name="Created at",
            value=f"`{datetime.strftime(role.created_at, '%d-%m-%Y')}` @ `{datetime.strftime(role.created_at, '%H:%M:%Y')}`"
        )
        
        embed.add_field(
            name="Members",
            value=f"`{len(role.members)}`"
        )

        attrs = inspect.getmembers(role.permissions, lambda a:not(inspect.isroutine(a)))

        attrs = [a for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]

        del attrs[0]
        del attrs[0]

        perms = {}

        for a in attrs:
            perms[a[0]] = a[1]

        final_perms = ""

        if perms['administrator'] is True:
            final_perms += "`Administrator`"

            embed.add_field(
                name="Key Permissions",
                value=final_perms
            )
        
        else:
            for perm, value in perms.items():
                if value is True:
                    final_perms += f"`{perm.replace('_', ' ').title()}` "
            
            embed.add_field(
                name="Key Permissions",
                value=final_perms
            )

        await ctx.send(embed=embed)



def setup(bot: Bot):
    bot.add_cog(Roles(bot))