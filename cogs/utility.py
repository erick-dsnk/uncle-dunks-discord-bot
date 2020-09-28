import discord
from discord.ext import commands
from newsapi import NewsApiClient
from time import sleep
import requests
from wikipedia import page


def get_newsapi_key():
    with open("tokens/newsapi_key.key", "r") as f:
        data = f.read()
        f.close()
    
    return data


def get_weather_api_key():
    with open("tokens/weather_api_token.key", "r") as f:
        data = f.read()
        f.close()
    
    return data


def get_rapid_api_key():
    with open("tokens/rapid_api_key.key", "r") as f:
        data = f.read()
        f.close()
    
    return data



newsapi_key = get_newsapi_key()
weather_key = get_weather_api_key()

newsapi = NewsApiClient(api_key=newsapi_key)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Returns the latency of the bot.
    @commands.command()
    async def ping(self, ctx):
        chnl = ctx.channel

        await chnl.send(f'Pong! Time took to respond: {round((self.bot.latency * 1000))}ms')

    # Help command
    @commands.command(aliases=['commands'])
    async def help(self, ctx):
        chnl = ctx.channel

        standard_help_msg = discord.Embed(
            title='Commands Help',
            description="""
                **Utility and Math**
                - octal <number>
                    (It calculates and sends the octal representation of the given number)
                
                - hex <number>
                    (It calculates and sends the hexadecimal code of the given number.)
                
                - binary <binary>
                    (It calculates and sends the binary code of the given number.)
                
                - ping
                    (Sends the latency of the bot.)
                
                - news <topic>
                    (It returns the top 5 headlines that it can find on that topic.)
                
                - topnews
                    (This one doesn't take a topic, it returns the top 5 most read articles it can find on that day.)
                
                - weather <city>
                    (It sends you basic current weather data, like temperature, humidity, and what it feels like)
                
                - wikisearch <topic>
                    (It fetches the top article on Wikipedia regarding that topic and sends it in chat)

                - coronavirus <country>
                    ( Aliases: cases, corona, covid. It sends you the current number of cases and deaths caused by COVID-19 in the country specified. Stay safe out there!)

                **Fun**
                - 8ball <question>
                    (It does what every Magic 8Ball does: it answers any question you have with crazy accuracy! Just kidding don't use it to make important decisions :) )
                
                - meme
                    (It sends a hot meme from Reddit)
                
                - joke
                    (Sends a top-notch joke from its extremely large joke database)
                
                - doggo
                    (It sends an image of a very cute doggo :3 )
            """,
            color=discord.Color.blurple
        )

        await chnl.send(embed=standard_help_msg)

    # Latest news on that subject from NewsAPI command
    @commands.command()
    async def news(self, ctx, topic):
        chnl = ctx.channel

        if topic != None:
            top_headlines = newsapi.get_top_headlines(
                q=f"{topic}",
                sources="bbc-news,the-verge,abc-news,cnn,fox-news,buzzfeed,google-news,cbs-news,entertainment-weekly,bleacher-report,nbc-news,new-york-magazine,the-wall-street-journal,the-washington-post",
                language="en"
            )

            articles = top_headlines['articles']

            await chnl.send(f"Here are the latest news on this subject: *{topic}*.")

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

        else:
            await chnl.send(":x: Missing required argument <city>")



    # Latest news in general from NewsAPI command
    @commands.command()
    async def topnews(self, ctx):
        
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
    @commands.command()
    async def weather(self, ctx, city):
        chnl = ctx.channel
        

        if city != None:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric'

            request = requests.get(url=url)

            data = request.json()

            # Get the basic weather description from the json
            additional_data = data['weather']
            desc = additional_data[0]['description']

            # The important weather data dictionary from the json file
            weather_data = data['main']

            # All the values of the data in the dictionary
            curr_temp = weather_data['temp']
            feels_like_temp = weather_data['feels_like']
            humidity = weather_data['humidity']
            atmospheric_pressure = weather_data['pressure']

            # Wind speed
            wind_data = data['wind']
            wind_speed = wind_data['speed']

            # Cloudiness
            clouds_data = data['clouds']
            cloudiness = clouds_data['all']

            # Getting the city name from the api so it's a little more clean
            city_data = data['name']

            # Initializing an embed to send a nicer looking composite of all the weather data
            embed = discord.Embed(
                title=f'Weather data for {city_data}',
                colour=discord.Color.from_rgb(43, 223, 255)
            )

            embed.add_field(
                name="**Basic weather**",
                value=f'**Description**: {desc}\n**Current temperature**: {curr_temp}\n**What it feels like**: {feels_like_temp}'
            )

            embed.add_field(
                name="**Wind speed, Humidity, etc**",
                value=f"**Wind speed**: {wind_speed} m/s\n**Humidity**: {humidity}%\n**Cloudiness**: {cloudiness}%\n**Atmospheric Pressure**: {round((atmospheric_pressure / 1013.25), 4)} atm ({atmospheric_pressure} hPa)"
            )

            await chnl.send(f"Ok, here's the weather information I found for {city_data}")
            sleep(1.2)
            await chnl.send(embed=embed)

        else:
            await chnl.send(":x: Missing required argument <city>")


    # Command for quickly searching wikipedia about a topic
    @commands.command()
    async def wikisearch(self, ctx, *, arg):
        chnl = ctx.channel

        if arg != None:
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
        
        else:
            await chnl.send(":x: Missing required argument <search_query>")


    @commands.command(aliases=['coronavirus', 'cases', 'covid'])
    async def corona(self, ctx, *, country):
        chnl = ctx.channel

        if country != "":

            try:
                url = "https://covid-193.p.rapidapi.com/statistics"

                querystring = {"country":country}

                headers = {
                    'x-rapidapi-host': "covid-193.p.rapidapi.com",
                    'x-rapidapi-key': get_rapid_api_key()
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                covid_data = response.json()

                data = covid_data['response']
                main_data = data[0]
                
                cases_data = main_data['cases']
                death_data = main_data['deaths']

                location = f"{main_data['country']}, {main_data['continent']}"
                total_cases = cases_data['total']
                new_cases = cases_data['new']
                healed_cases = cases_data['recovered']
                active_cases = cases_data['active']

                new_deaths = death_data['new']
                total_deaths = death_data['total']

                date = main_data['day']


                embed = discord.Embed(
                    title=f"COVID-19 Information for {main_data['country']}",
                    description=f'Total cases: {total_cases}\nActive Cases: {active_cases}\nNew cases: {new_cases}\nRecovered: {healed_cases}\n-----------------------------------------------\nTotal deaths: {total_deaths}\nNew Deaths: {new_deaths}'
                )

                await chnl.send(embed=embed)

            
            except Exception as e:
                await chnl.send(":x: Sorry, I can't seem to fetch any information about it.")

                print(e)
    

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s avatar")

        embed.set_image(url=member.avatar_url)

        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Utility(bot))