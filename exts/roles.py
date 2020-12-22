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
        if type(role) == str:
            for r in ctx.guild.roles:
                if role.lower() in r.name.lower():
                    await member.add_roles(r)

                    embed = discord.Embed(
                        title=":white_check_mark: Success!",
                        description=f"Added role to {member.mention}!",
                        color=discord.Color.green()
                    )

                    await ctx.send(embed=embed)

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
                embed = discord.Embed(
                    title=":x: Oops!",
                    description="Couldn't find any role with that ID!",
                    color=discord.Color.red()
                )

                await ctx.send(embed=embed)

        elif type(role) == Role:
            await member.add_roles(role)

            embed = discord.Embed(
                title=":white_check_mark: Success!",
                description=f"Added role to {member.mention}!",
                color=discord.Color.green()
            )

            await ctx.send(embed=embed)
    

    @commands.has_permissions(manage_roles=True)
    @commands.command(aliases=['rr'])
    async def removerole(self, ctx: Context, member: discord.Member, role) -> None:
        '''
        Remove a role from a user!
        Role can be in the form of an ID, name, or a role mention!
        '''
        if type(role) == str:
            for r in ctx.guild.roles:
                if role.lower() in r.name.lower():
                    await member.remove_roles(r)

                    embed = discord.Embed(
                        title=":white_check_mark: Success!",
                        description=f"Removed role from {member.mention}!",
                        color=discord.Color.green()
                    )

                    await ctx.send(embed=embed)


        elif type(role) == int:
            r = get(ctx.guild.roles, id=role)

            if r:
                await member.remove_roles(r)

                embed = discord.Embed(
                    title=":white_check_mark: Success!",
                    description=f"Removed role from {member.mention}!",
                    color=discord.Color.green()
                )

                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title=":x: Oops!",
                    description="Couldn't find any role with that ID!",
                    color=discord.Color.red()
                )

                await ctx.send(embed=embed)

        elif type(role) == Role:
            await member.remove_roles(role)

            embed = discord.Embed(
                title=":white_check_mark: Success!",
                description=f"Removed role from {member.mention}!",
                color=discord.Color.green()
            )

            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Roles(bot))