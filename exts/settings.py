import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
import json

class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setwelcomechannel(self, ctx: Context, channel):
        guild = str(ctx.guild.id)


        await ctx.channel.send(f":white_check_mark: Successfully set welcome channel to #{channel}")


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setwelcomemessage(self, ctx, *, msg):
        settings = None

        guild = str(ctx.guild.id)

        with open('settings.json', 'r') as f:
            data = json.load(f)

            if guild in data['server-settings']:
                data['server-settings'][guild]['welcome_message'] = str(msg)
            
            else:
                data['server-settings'].append({guild: {}})
                data['server-settings'][guild]['welcome_message'] = str(msg)

        with open('settings.json', 'w') as f:
            obj = json.dumps(data, indent=4)

            f.write(obj)
        
        await ctx.channel.send(":white_check_mark: Successfully set welcome message!")


def setup(bot):
    bot.add_cog(Settings(bot))