#   Copyright 2020 Tabacaru Eric
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


'''
Uncle Dunk's Bot v1.6.3
'''


import discord
from discord.ext import commands
from discord.ext.commands import Bot
from pretty_help import PrettyHelp
from discord import Message
from exts.database import settings_collection


def determine_prefix(bot: Bot, message: Message):
    if message.guild:
        settings = settings_collection.find_one({"_id": message.guild.id})['settings']

        if 'prefix' in settings.keys():
            return settings['prefix']
        
        else:
            return '-'
    
    else:
        return '-'


intents = discord.Intents.all()
client = commands.Bot(command_prefix=determine_prefix, intents=intents)

client.help_command = PrettyHelp()

################ GET TOKEN FUNCTION ###############
def get_token():
    with open("tokens/token.key", 'r') as f:
        data = f.read()
        f.close()
    
    return data
############################################

################## COGS ####################
# client.load_extension('exts.code_eval')   ->  represented security issues
client.load_extension('exts.entertainment')
client.load_extension('exts.events')
client.load_extension('exts.games')
client.load_extension('exts.moderation')
client.load_extension('exts.utility')
client.load_extension('exts.economy')
client.load_extension('exts.settings')
client.load_extension('exts.suggestions')
client.load_extension('exts.managing')
client.load_extension('exts.music')
############################################

client.run(get_token())
