import discord
from discord.ext import commands
from random import randint, choice
import praw
import requests
from time import sleep


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
    @commands.command(pass_context=True, aliases=["8ball"])
    async def _8ball(self, ctx, *, q):
        chnl = ctx.channel

        if q != None:

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

            await chnl.send(response)
        
        else:
            await chnl.send(":x: Missing required argument: <question>")


    # Meme from reddit command
    @commands.command(pass_context=True)
    async def meme(self, ctx):
        memes = reddit_instance.subreddit('memes').hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in memes if not x.stickied)

        chnl = ctx.channel

        await chnl.send(submission.url)


    # A cute doggo from reddit command :3
    @commands.command(pass_context=True)
    async def doggo(self, ctx):
        dogs = reddit_instance.subreddit('doggos').hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in dogs if not x.stickied)
        
        chnl = ctx.channel

        await chnl.send(submission.url)


    # Jokes from JokeAPIv2 command
    @commands.command(pass_context=True)
    async def joke(self, ctx):
        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

        headers = {
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com",
            'x-rapidapi-key': get_rapid_api_key()
        }

        req = requests.get(url=url, headers=headers)

        joke_data = req.json()


        openers = [
            "Okay, here comes a good one...",
            "I'm a bit rusty but I'll give it a shot.",
            "Really?? No one has wanted to hear my jokes in so long, I'll be glad to tell you one!",
            "Hmm, let me think... Oh I know just the one!",
            "Ok fine, I'll tell you one, but don't make a habit out of it!"
        ]

        opener = choice(openers)

        chnl = ctx.channel

        if joke_data['type'] == "single":
            await chnl.send(opener)

            sleep(2.2)

            await chnl.send(f"**{joke_data['joke']}**")

        elif joke_data['type'] == "twopart":
            await chnl.send(opener)

            sleep(2.2)

            await chnl.send(f"**{joke_data['setup']}**")

            sleep(3.0)

            await chnl.send(f"**{joke_data['delivery']}**")
        
        else:
            print(f"Another type of joke found: {joke_data['type']}")


def setup(bot):
    bot.add_cog(Entertainment(bot))