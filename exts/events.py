import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from discord.ext.commands.errors import CommandNotFound
import difflib
from exts.database import economy_collection


all_commands = [
    'help',
    'rps',
    'tictactoe',
    'joke',
    'meme',
    'doggo',
    'binary',
    'hexadecimal',
    'octal',
    'kick',
    'ban',
    'mute',
    'unmute',
    'vcmute',
    'vcunmute',
    'corona',
    'weather',
    'wikisearch',
    'news',
    'ping',
    'avatar',
    'botinfo',
    'userinfo',
    'serverinfo',
    'eval'
]


def setup_database(client):
    for guild in client.guilds:
        if not economy_collection.find_one({"_id": guild.id}):
            members = []

            for member in guild.members:
                members.append(
                    {"id": member.id, "money": 0}
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
        possible_matches = difflib.get_close_matches(ctx.message.content.split()[0].strip("-"), all_commands)
        
        if isinstance(error, CommandNotFound):
            if possible_matches:
                await ctx.send(f':x: That\'s not a command! Did you mean `-{possible_matches[0]}`?')

            else:
                await ctx.send(f':x: That\'s not a command!')
        
        else:
            print(error)

def setup(bot):
    bot.add_cog(Events(bot))
