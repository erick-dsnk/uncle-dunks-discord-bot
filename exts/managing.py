import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context


class Manager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def announce(self, ctx: Context, channel: discord.TextChannel, *, message: str):
        '''
        Make an announcement with a fancy embed containing your important message.
        '''
        
        embed = discord.Embed(
            title=":loudspeaker: **Important announcement!**",
            description=f"{message}",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Announcement made by {ctx.author.name}#{ctx.author.discriminator}.")

        await channel.send(embed=embed)
    

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def annoeveryone(self, ctx: Context, channel: discord.TextChannel, *, message: str):
        '''
        Does the same thing as `announce` but also tags `@everyone`.
        '''
        
        embed = discord.Embed(
            title=":loudspeaker: **Important announcement!**",
            description=f"{message}",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Announcement made by {ctx.author.name}#{ctx.author.discriminator}.")

        await channel.send("@everyone", embed=embed)
    

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def annohere(self, ctx: Context, channel: discord.TextChannel, *, message: str):
        '''
        Does the same thing as `announce` but also tags `@here`
        '''
        
        embed = discord.Embed(
            title=":loudspeaker: **Important announcement!**",
            description=f"{message}",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Announcement made by {ctx.author.name}#{ctx.author.discriminator}.")

        await channel.send("@here", embed=embed)


def setup(bot: Bot):
    bot.add_cog(Manager(Bot))