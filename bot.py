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




import discord
from discord.ext import commands
from discord.utils import get
import praw
from random import randint, choice
from time import sleep
import requests
from wikipedia import page
from datetime import datetime


client = commands.Bot(command_prefix = '-')


################ GET TOKEN FUNCTION ###############
def get_token():
    with open("tokens/token.key", 'r') as f:
        data = f.read()
        f.close()
    
    return data

token = get_token()
############################################


# Bot ready event
@client.event
async def on_ready():
    print("Uncle Dunk's bot is in the house and he ain't leavin")


################## COGS ####################
client.load_extension('cogs.moderation')
client.load_extension('cogs.entertainment')
client.load_extension('cogs.utility')
client.load_extension('cogs.math')
client.load_extension('cogs.music')
############################################



client.run(token)