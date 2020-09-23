import discord
from discord.ext import commands
import youtube_dl
from helpers.yt_searcher import search
from discord.utils import get
import shutil
import os


#if not discord.opus.is_loaded():
#    discord.opus.load_opus('libopus.so')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}


    @commands.command()
    async def join(self, ctx):
        global voice
        
        chnl = ctx.message.author.voice.channel

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(chnl)
        
        else:
            voice = await chnl.connect()
        
        await ctx.channel.send(f":white_check_mark: Joined {chnl}")
    

    @commands.command()
    async def leave(self, ctx):
        chnl = ctx.message.author.voice.channel

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.channel.send(f":white_check_mark: Left from {chnl}")
    

    @commands.command(aliases=['p'])
    async def play(self, ctx, url):        
        def check_queue():
            Queue_infile = os.path.isdir("./Queue")

            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))

                length = len(os.listdir(DIR))

                still_q = length - 1

                try:
                    first_file = os.listdir(DIR)[0]
                
                except:
                    print('No more queued songs.')
                    self.queues.clear()
                    return
                
                main_loc = os.path.dirname(os.path.realpath(__file__))

                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)

                if length != 0:
                    print('Song finished, playing next in queue.')

                    print(f"Songs left in queue: {still_q}")

                    song_there = os.path.isfile("song.mp3")

                    if song_there:
                        os.remove("song.mp3")
                    
                    shutil.move(song_path, main_loc)

                    for file in os.listdir('./'):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                
                    voice.source = discord.PCMVolumeTransformer(voice.source)

                    voice.source.volume = 0.3

                else:
                    self.queues.clear()

                    return
                

            else:
                self.queues.clear()

                print('No songs left in queue.')
        
        song_there = os.path.isfile("song.mp3")

        try:
            if song_there:
                os.remove("song.mp3")
                self.queues.clear()

        except PermissionError as e:
            print("Trying to delete song file but it is being played.")

            await ctx.channel.send(':x: Error: music still playing.')

            return

        Queue_infile = os.path.isdir('./Queue')

        try:
            Queue_folder = "./Queue"

            if Queue_infile is True:
                print('Removed old queue folder.')

                shutil.rmtree(Queue_folder)
            
        except:
            print('No old queue folder.')
        

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ytdl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,\
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            print('Downloading audio')

            ydl.download([url])
        
        name = ""

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file

                print(f"Renamed file {name}")

                os.rename(file, 'song.mp3')
            
        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.3

        nname = name.rsplit("-", 2)

        await ctx.channel.send(f":musical_note: Playing {nname[0]}")


    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()

            print('Paused music')

            await ctx.channel.send(':white_check_mark: Music paused.')
        
        else:
            await ctx.channel.send(':x: No music is playing!')
        

    @commands.command(aliases=['resume'])
    async def unpause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()

            print('Resumed music')

            await ctx.channel.send(':white_check_mark: Unpaused music.')
        
        else:
            await ctx.channel.send(':x: Music is not paused!')
    
    @commands.command(aliases=['pass'])
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        self.queues.clear()

        if voice and voice.is_playing():
            voice.stop()

            print('Stopped music')

            await ctx.channel.send(':white_check_mark: Skipped this track.')
        
        else:
            await ctx.channel.send(':x: No track is playing!')

    @commands.command(aliases=['q'])
    async def queue(self, ctx, url):
        Queue_infile = os.path.isdir('./Queue')

        if Queue_infile is False:
            os.mkdir('Queue')
        
        DIR = os.path.abspath(os.path.realpath("Queue"))

        q_num = len(os.listdir(DIR))
        q_num += 1

        add_q = True

        while add_q:
            if q_num in self.queues:
                q_num += 1
        
            else:
                add_q = False
                self.queues[q_num] = q_num
        
        queue_path = os.path.abspath(os.path.realpath('Queue') + f"\\song{q_num}.%(ext)s")

        ytdl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            print('Downloading audio')
            
            ydl.download([url])

        await ctx.channel.send(':white_check_mark: Added song to queue!')




def setup(bot):
    bot.add_cog(Music(bot))

