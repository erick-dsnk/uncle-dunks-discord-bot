import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from random import choice


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def rps(self, ctx: Context, user_choice: str):
        possibilities = ['rock', 'scissors', 'paper']

        win_conditions = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        bot_choice = choice(possibilities)

        if user_choice == bot_choice:
            final_statement = "Tie! Nobody wins."

        elif user_choice == win_conditions[bot_choice]:
            final_statement = "You lose! Good luck next time."

        elif user_choice != win_conditions[bot_choice]:
            final_statement = "You win! Good job!"

        embed = discord.Embed(
            title="Rock, Paper, Scissors!",
            color=discord.Color.blurple(),
            description=f"Your choice: `{user_choice.title()}`\nMy choice: `{bot_choice.title()}`\n**{final_statement}**"
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def tictactoe(self, ctx: Context):
        pass


def setup(bot):
    bot.add_cog(Games(bot))