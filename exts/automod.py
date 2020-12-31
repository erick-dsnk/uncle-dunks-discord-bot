import discord
from discord.ext.commands import Cog, Bot
from exts.database import settings_collection

class Automod(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener
    async def on_message(self, message: discord.Message):
        settings = settings_collection.find_one(
            {"_id": message.guild.id}
        )['settings']

        if 'automod' in settings.keys():
            if settings['automod'] == 'on':
                if 'bad_patterns' in settings.keys():
                    patterns = settings['bad_patterns']

                    for word in message.content.split(' '):
                        if word.lower() in patterns:
                            await message.delete()

                else:
                    pass
            
            else:
                pass
        

                