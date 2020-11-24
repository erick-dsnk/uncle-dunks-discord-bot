import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from discord.ext.commands.errors import CommandNotFound
from discord.utils import get
from exts.database import economy_collection, settings_collection


def setup_database(client: Bot):
    for guild in client.guilds:
        if not economy_collection.find_one({"_id": guild.id}):
            members = []

            for member in guild.members:
                members.append(
                    {"id": member.id, "money": 0, "bank": 0}
                )

            economy_collection.insert_one(
                {
                    "_id": guild.id,
                    "name": guild.name,
                    "members": members
                }
            )
        
        else:
            pass
        

        if not settings_collection.find_one({"_id": guild.id}):
            settings_collection.insert_one(
                {
                    "_id": guild.id,
                    "name": guild.name,
                    "settings": {}
                }
            )
        
        else:
            pass
        


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    

    @Cog.listener()
    async def on_ready(self):
        print('Uncle Dunk\'s bot is in the house and he ain\'t leaving')
        await self.bot.change_presence(status=discord.Status.dnd, activity=Game(name="||| -help to see a list of commands! |||"))
        setup_database(self.bot)

    
    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(f':x: That\'s not a command!')
        
        else:
            print(error)
    

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        members_data = economy_collection.find_one({"_id": member.guild.id})['members']

        members_data.append({"id": member.id, "money": 0, "bank": 0})

        economy_collection.find_one_and_update({"_id": member.guild.id}, {"$set": {"members": members_data}})


        settings = settings_collection.find_one({"_id": member.guild.id})['settings']

        if 'welcome_channel' in settings.keys():
            welcome_channel = get(member.guild.text_channels, id=settings['welcome_channel'])

            embed = discord.Embed(
                title=f"**{member.guild.name}**",
                description=f"Welcome to {member.guild.name}! :partying_face:",
                color=discord.Color.green()
            )

            await welcome_channel.send(embed=embed)
        
        else:
            pass


    @Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        members_data = economy_collection.find_one({"_id": member.guild.id})['members']

        i = 0

        for user in members_data:
            if user['id'] == member.id:
                del members_data[i]
                break
            
            else:
                pass

            i += 1
        
        economy_collection.find_one_and_update({"_id": member.guild.id}, {"$set": {"members": members_data}})


    @Cog.listener()
    async def on_guild_join(self, guild):
        setup_database(self.bot)
    
    @Cog.listener()
    async def on_guild_remove(self, guild):
        economy_collection.delete_one({"_id": guild.id})
        settings_collection.delete_one({"_id": guild.id})


def setup(bot):
    bot.add_cog(Events(bot))
