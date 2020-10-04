from typing import Dict, Any
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from datetime import date
import requests


class Apod:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.url = "https://api.nasa.gov/planetary/apod"
        self.date = date.today().strftime('%Y-%m-%d')
    
    def fetch_apod_data(self) -> Dict:
        headers = {
            'api_key': self.api_key,
            'date': self.date,
            'hd': True
        }

        response = requests.get(
            url=self.url,
            params=headers
        ).json()

        return response
    

    def __call__(self) -> Any:
        data = self.fetch_apod_data()
        return data['hdurl'], data['title']



class ApodCommand(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
        with open('tokens/nasa_api_key.key', 'r') as f:
            api_key = f.read()

        self.apod_instance = Apod(api_key=api_key)
    

    @commands.command(aliases=['space', 'spaceimg', 'spaceimage', 'apodimg', 'apodimage'])
    async def apod(self, ctx: Context):
        url, title = self.apod_instance()

        embed = discord.Embed(
            title=title,
            color=discord.Color.dark_blue()
        )

        embed.set_image(url=url)

        await ctx.send(embed=embed)