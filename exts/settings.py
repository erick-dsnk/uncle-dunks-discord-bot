import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, Cog
from discord.utils import get
from exts.database import settings_collection


class Settings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    

    @commands.command()
    async def setwelcomechannel(self, ctx: Context, channel):
        if isinstance(channel, discord.TextChannel):
            channel_id = channel.id
        
        else:
            channel_id = channel
        
        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        try:
            channel_id = int(channel_id)
        except:
            await ctx.send(":x: That's not a channel!")
            
            return
        
        settings['welcome_channel'] = channel_id

        settings_collection.find_one_and_update({"_id": ctx.guild.id}, {"$set": {"settings": settings}})

    
def setup(bot):
    bot.add_cog(Settings(bot))