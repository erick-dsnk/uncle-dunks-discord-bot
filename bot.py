import discord
from discord.ext import commands
import praw
from random import randint, choice
from newsapi import NewsApiClient
from time import sleep
import requests
from wikipedia import page


client = commands.Bot(command_prefix = '-')


################ GET TOKEN FUNCTIONS (SECURITY REASONS) ###############
def get_token():
    with open("token.txt", 'r') as f:
        data = f.read()
        f.close()
    
    return data

def get_client_id():
    with open("client_id.txt", "r") as f:
        data = f.read()
        f.close()
    
    return data

def get_client_secret():
    with open("client_secret.txt", "r") as f:
        data = f.read()
        f.close()
    
    return data

def get_rapid_api_key():
    with open("rapid_api_key.txt", "r") as f:
        data = f.read()
        f.close()
    
    return data

def get_newsapi_key():
    with open("newsapi_key.txt", "r") as f:
        data = f.read()
        f.close()
    
    return data

############################################


############ TOKENS / API KEYS #############
token = get_token()
client_id = get_client_id()
client_secret = get_client_secret()
newsapi_key = get_newsapi_key()
############################################


# Reddit instance for meme command
reddit_instance = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="Uncle Dunk's Bot/0.0.1 by u/dsnk24"
)

# NewsAPI instance for news and topnews command
newsapi = NewsApiClient(api_key=newsapi_key)


############## PREDEFINED DISCORD EVENTS ##################

# Bot ready event
@client.event
async def on_ready():
    print("Bot is ready.")

##########################################################


############## MATH / UTILITY COMMANDS ###################

# Octal representation of a number command
@client.command(pass_context=True)
async def octal(ctx, arg):
    chnl = ctx.channel
    
    try:
        arg = int(arg)
    except Exception as e:
        print(f"An error occured while handling an octal command: {e}")

    if type(arg) == int:
        await chnl.send("The octal representation of that number is {}.".format(oct(arg)))
    else:
        await chnl.send(f"{arg} is not an integer.")


# Binary code of a number command
@client.command(pass_context=True)
async def binary(ctx, arg):
    chnl = ctx.channel

    try:
        arg = int(arg)
    except Exception as e:
        print(f"An error occured while handling a binary command: {e}")


    if type(arg) == int:
        await chnl.send("The binary code of that number is {0:b}".format(arg))
    else:
        await chnl.send(f"{arg} is not an integer.")


# Hexadecimal code of a number command
@client.command(pass_context=True, aliases=["hex"])
async def hexadecimal(ctx, arg):
    chnl = ctx.channel

    try:
        arg = int(arg)
    except Exception as e:
        print(f"An error occured while handling a hexadecimal command: {e}")
    

    if type(arg) == int:
        await chnl.send("The hexadecimal code of that number is {}".format(hex(arg)))
    else:
        await chnl.send(f"{arg} is not an integer.")


# Returns the latency of the bot.
@client.command(pass_context=True)
async def ping(ctx):
    chnl = ctx.channel

    await chnl.send(f'Pong! Time took to respond: {round((client.latency * 1000), 0)}')


# Latest news on that subject from NewsAPI command
@client.command(pass_context=True)
async def news(ctx, arg):

    top_headlines = newsapi.get_top_headlines(
        q=f"{arg}",
        sources="bbc-news,the-verge,abc-news,cnn,fox-news,buzzfeed,google-news,cbs-news,entertainment-weekly,bleacher-report,nbc-news,new-york-magazine,the-wall-street-journal,the-washington-post",
        language="en"
    )

    articles = top_headlines['articles']

    chnl = ctx.channel

    await chnl.send(f"Here are the latest news on this subject: *{arg}*.")

    sleep(1.3)

    if len(articles) > 5:
        iterations = 5
    else:
        iterations = len(articles)

    for i in range(iterations):
        article = articles[i]

        await chnl.send(
            f"**Headline #{(i + 1)}: {article['title']}**\n{article['description']}\n{article['url']}"
        )

        if i != (iterations - 1):
            await chnl.send("-----------------------------------------------------------------")
        else:
            pass

        sleep(3.7)


# Latest news in general from NewsAPI command
@client.command(pass_context=True)
async def topnews(ctx):
    
    top_headlines = newsapi.get_top_headlines(
        sources="bbc-news,the-verge,abc-news,cnn,fox-news,buzzfeed,google-news,cbs-news,entertainment-weekly,bleacher-report,nbc-news,new-york-magazine,the-wall-street-journal,the-washington-post",
        language="en"
    )


    articles = top_headlines['articles']

    chnl = ctx.channel

    await chnl.send(f"Here are the top headlines I could find:")

    sleep(1.3)


    if len(articles) > 5:
        iterations = 5
    else:
        iterations = len(articles)


    for i in range(iterations):
        article = articles[i]

        await chnl.send(
            f"**Headline #{(i + 1)}: {article['title']}**\n{article['description']}\n{article['url']}"
        )

        if i != (iterations - 1):
            await chnl.send("-----------------------------------------------------------------")
        else:
            pass

        sleep(3.7)


# Weather command using the OpenWeatherMap API
@client.command(pass_context=True)
async def weather(ctx, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=57a28fdb4970e359193164a1e8f77aa7&units=metric'

    chnl = ctx.channel

    request = requests.get(url=url)

    data = request.json()

    weather_data = data['main']

    curr_temp = weather_data['temp']
    feels_like_temp = weather_data['feels_like']
    humidity = weather_data['humidity']

    city_data = data['name']

    await chnl.send(f"Ok, here's the current weather data for {city_data}:")
    sleep(1.2)
    await chnl.send(
        f"Current temperature: {curr_temp} Celsius\nIt feels like: {feels_like_temp} Celsius\nHumidity: {humidity}%"
    )


# Command for quickly searching wikipedia about a topic
@client.command(pass_context=True)
async def wikisearch(ctx, *, arg):
    chnl = ctx.channel

    wiki_page = page(arg)

    title = wiki_page.title
    desc = (wiki_page.content[:300] + "...") if len(wiki_page.content) > 303 else wiki_page.content
    url = wiki_page.url

    await chnl.send(
        f"Here's what I found on Wikipedia about *{arg}*:"
    )

    sleep(2.0)

    await chnl.send(
        f"**{title}**\n{desc}\n\nFind out more about it here: {url}"
    )




    
###########################################################





################ ENTERTAINMENT COMMANDS ###################

# Magic 8 Ball command
@client.command(pass_context=True, aliases=["8ball"])
async def _8ball(ctx, *, q):
    chnl = ctx.channel

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


# Meme from reddit command
@client.command(pass_context=True)
async def meme(ctx):
    memes = reddit_instance.subreddit('memes').hot()

    pick_number = randint(0, 10)

    for i in range(0, pick_number):
        submission = next(x for x in memes if not x.stickied)

    chnl = ctx.channel

    await chnl.send(submission.url)


# Jokes from JokeAPIv2 command
@client.command(pass_context=True)
async def joke(ctx):
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

#############################################


client.run(token)