import discord
from discord.ext import commands
import json


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Uncle Dunk\'s bot is in the house and he ain\'t leaving')
        await self.bot.change_presence(activity=discord.Activity(name="||| -help to show the list of commands! |||"), status=discord.Status.dnd)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = str(member.guild.id)

        welcome_channel = None
        welcome_message = None

        with open('settings.json', 'r') as f:
            data = json.load(f)

            if guild in data['server-settings']:
                settings = data['server-settings'][guild]

                chnl_id = int(settings['welcome_channel'])

                welcome_message = settings['welcome_message']

                if '@mention@' in welcome_message:
                    welcome_message.replace('@mention@', member.mention)

                welcome_channel = discord.utils.get(member.guild.channels, id=chnl_id)


        if welcome_channel:
            if welcome_message:
                await welcome_channel.send(welcome_message)
            else:
                await welcome_channel.send(f"Welcome {member.mention}!")

        else:
            pass


def setup(bot):
    bot.add_cog(Events(bot))