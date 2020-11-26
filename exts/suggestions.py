import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from exts.database import settings_collection


class Suggestions(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    
    @commands.command()
    async def feature(self, ctx: Context, *, suggestion: str):
        '''
        Suggest a feature or command to the creator of the bot!
        '''
        embed = discord.Embed(
            title="Feature request!",
            description=f"""
You got a feature request from `{ctx.author.name}#{ctx.author.discriminator}`
```
{suggestion}
```
""",
            color=discord.Color.blurple()
        )

        creator = self.bot.get_user(419022467210936330)

        if creator != None:
            dm = creator.create_dm()

            await dm.send(embed=embed)
        
        else:
            pass
            
        await ctx.send(":white_check_mark: Your request has been sent to the creator!")
    

    @commands.command()
    async def suggest(self, ctx: Context, *, suggestion: str):
        embed = discord.Embed(
            title="Server suggestion",
            description=f"""
You have received a suggestion from `{ctx.author.name}#{ctx.author.discriminator}`
```
{suggestion}
```
""",
            color=discord.Color.green()
        )

        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        if 'suggestion_channel' in settings.keys():
            channel = discord.utils.get(ctx.guild.text_channels, id=settings['suggestion_channel'])

            if channel != None:
                await channel.send(embed=embed)
                await ctx.send(":white_check_mark: Your request has been sent to the staff of this server!")
            
            else:
                await ctx.send(":x: The suggestion channel doesn't exist or was deleted. Ask a moderator to set one with `-setsuggestionchannel <channel_id>`.")

        else:
            await ctx.send(":x: No suggestion channel is set. Ask a moderator to set one with `-setsuggestionchannel <channel_id>`")