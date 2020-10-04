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
import os

client = commands.Bot(command_prefix = '-')

client.remove_command('help')


################ GET TOKEN FUNCTION ###############
def get_token():
    with open("tokens/token.key", 'r') as f:
        data = f.read()
        f.close()
    
    return data

token = get_token()
############################################

################## COGS ####################
for ext in os.listdir('./exts'):
    if ext.endswith('.py'):
        client.load_extension(f'exts.{ext.strip(".py")}')
############################################



client.run(token)