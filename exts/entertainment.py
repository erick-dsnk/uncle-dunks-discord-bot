import random
import discord
from discord.ext import commands
from random import randint, choice
from discord.ext.commands import Context
import praw
import requests


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
    @commands.command(name="8ball")
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
        sub = random.choice([
            'memes',
            'ComedyCemetery',
            'MemeEconomy',
            'dankmemes',
            'terriblefacebookmemes',
            'wholesomememes',
            'okbuddyretard',
            'comedyheaven'
        ])

        memes = reddit_instance.subreddit(sub).hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in memes if not x.stickied)

        chnl = ctx.channel

        await chnl.send(submission.url)


    # A cute doggo from reddit command :3
    @commands.command(aliases=['dog', 'doggie', 'pup', 'pupper', 'puppy'])
    async def doggo(self, ctx):
        '''
        Sends you a picture of a cute doggo :3
        '''
        sub = random.choice([
            'doggos',
            'dogpictures',
            'dogs',
            'puppies',
            'goldenretrievers'
        ])

        dogs = reddit_instance.subreddit(sub).hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in dogs if not x.stickied)
        
        chnl = ctx.channel

        await chnl.send(submission.url)
    

    @commands.command(aliases=['kitten', 'kitty'])
    async def cat(self, ctx):
        '''
        Sends you a picture of a cute kitty :3
        '''
        sub = random.choice([
            'JellyBeanToes',
            'CatsStandingUp',
            'Kittens',
            'Cats',
            'CatsInBusinessAttire',
            'TuckedInKitties'
        ])
        
        cats = reddit_instance.subreddit(sub).hot()

        pick_number = randint(0, 10)

        for i in range(0, pick_number):
            submission = next(x for x in cats if not x.stickied)
        
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
    

    @commands.command(aliases=['poke'])
    async def pokemon(self, ctx: Context, poke: str):
        '''
        Get information about a Pokemon!
        '''
        base_url = "https://pokeapi.co/api/v2/pokemon/"

        response = requests.get(base_url + poke)

        if response.status_code == 404:
            embed = discord.Embed(
                title="Darn!",
                description="Sorry, can't seem to find any information about that Pokemon. Check your spelling and try again!",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)

        else:
            response = response.json()

            abilities = response['abilities']
            types = response['types']
            stats = response['stats']
            moves = response['moves']

            ability_field = ""
            type_field = ""
            stat_field = ""
            move_field = ""

            for ability in abilities:
                ability_field += ability['ability']['name'].title()
                ability_field += "\n"

            for _type in types:
                type_field += _type['type']['name'].title()
                type_field += "\n"

            for stat in stats:
                stat_field += stat['stat']['name'].title() + "\t\t" + str(stat['base_stat'])
                stat_field += "\n"

            if len(moves) > 6:
                for i in range(5):
                    move_field += moves[i]['move']['name'].title()
                    move_field += "\n"
                
                move_field += "..."
            
            else:
                for move in moves:
                    move_field += move['move']['name'].title()
                    move_field += "\n"

            embed = discord.Embed(
                title=f"{poke.title()}",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="**Height**",
                value=f"{response['height']}",
                inline=True
            )

            embed.add_field(
                name="**Weight**",
                value=f"{response['weight']}",
                inline=True
            )

            embed.add_field(
                name=f"**Types [{len(types)}**",
                value=f"{type_field}",
                inline=True
            )

            embed.add_field(
                name=f"**Abilities [{len(abilities)}]**",
                value=f"{ability_field}",
                inline=True
            )

            embed.add_field(
                name=f"**Stats**",
                value=f"{stat_field}",
                inline=True
            )
            
            embed.add_field(
                name=f"**Moves**",
                value=f"{move_field}",
                inline=True
            )

            embed.set_image(url=response['sprites']['back_default'])

            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Entertainment(bot))
