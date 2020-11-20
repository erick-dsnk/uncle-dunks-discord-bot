import discord
from discord.ext import commands
from random import randint, choice
from discord.ext.commands import Context
import praw
import requests
import asyncio


def get_client_id():
    with open("tokens/client_id.key", "r") as f:
        data = f.read()
        f.close()
    
    return data

def get_client_secret():
    with open("tokens/client_secret.key", "r") as f:
        data = f.read()
        f.close()
    
    return data

def get_rapid_api_key():
    with open("tokens/rapid_api_key.key", "r") as f:
        data = f.read()
        f.close()
    
    return data



client_id = get_client_id()
client_secret = get_client_secret()

# Reddit instance for meme command
reddit_instance = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="Uncle Dunk's Bot/0.0.1 by u/dsnk24"
)

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Magic 8 Ball command
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, q = ""):
        '''
        Shake the Magic 8 Ball and get an answer to your question
        Usage: `-8ball Am I a good cookie?`
        '''
        chnl = ctx.channel

        if q != "":

            answers = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes – definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."
            ]

            response = choice(answers)

            embed = discord.Embed(
                color=discord.Color.blurple()
            )

            embed.add_field(
                name=":question: Question",
                value=f"*{q}*"
            )

            embed.add_field(
                name=":a: Answer",
                value=f"*{response}*"
            )
        
            await chnl.send(embed=embed)

        else:
            await chnl.send(":x: Missing required argument: `question`")


    # Meme from reddit command
    @commands.command()
    async def meme(self, ctx):
        '''
        It sends you a hot meme off Reddit!
        '''
        memes = reddit_instance.subreddit('memes').hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in memes if not x.stickied)

        chnl = ctx.channel

        await chnl.send(submission.url)


    # A cute doggo from reddit command :3
    @commands.command()
    async def doggo(self, ctx):
        '''
        Sends you a picture of a cute doggo :3
        '''
        dogs = reddit_instance.subreddit('doggos').hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in dogs if not x.stickied)
        
        chnl = ctx.channel

        await chnl.send(submission.url)


    # Jokes from JokeAPIv2 command
    @commands.command()
    async def joke(self, ctx):
        '''
        Tells you a top-notch joke.
        '''
        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

        headers = {
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com",
            'x-rapidapi-key': get_rapid_api_key()
        }

        req = requests.get(url=url, headers=headers)

        joke_data = req.json()

        answers = [
            'Here\'s a good one!',
            'Ooo this is a spicy one!',
            'I\'m still laughing at this one!'
        ]

        if joke_data['type'] == 'single':
            embed = discord.Embed(
                title=choice(answers),
                color=discord.Color.blurple(),
                description=joke_data['joke']
            )
        
        elif joke_data['type'] == 'twopart':
            embed = discord.Embed(
                title=choice(answers),
                color=discord.Color.blurple(),
                description=f"{joke_data['setup']}\n{joke_data['delivery']}"
            )


        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Entertainment(bot))
