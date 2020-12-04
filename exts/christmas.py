import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
import os
from random import choice


class Christmas(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def christmasplay(self, ctx: Context) -> None:
        '''
        Continously play hundreds of Christmas songs in that voice channel!
        '''
        playing = True

        vc = ctx.author.voice.channel

        if vc is not None:
            vc = await vc.connect()

            songs = os.listdir(os.path.abspath('christmas-music'))

            print(vc)
            print(songs)
            print(vc.is_playing())

            while playing:
                if not vc.is_playing():
                    vc.play(
                        discord.FFmpegPCMAudio(
                            os.path.abspath(
                                os.path.join("christmas-music", choice(songs))
                            )
                        )
                    )
            
        else:
            await ctx.send(':x: You\'re not in a voice channel!')


def setup(bot: Bot):
    bot.add_cog(Christmas(bot))