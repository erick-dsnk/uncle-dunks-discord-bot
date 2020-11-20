import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from random import choice


class Games(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.command()
    async def rps(self, ctx: Context, user_choice: str):
        '''
        Play a good game of Rock, Paper, Scissors with Uncle Dunk!
        Choices: `rock`, `paper`, `scissors`
        '''
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
        '''
        Play a game of Tic Tac Toe against Uncle Dunk! (WIP)
        '''
        table = """
        1      2      3
     ______________________
     |      |      |      |
  1  |  {11}  |  {12}  |  {13}  |
     |______|______|______|
     |      |      |      |
  2  |  {21}  |  {22}  |  {23}  |
     |______|______|______|
     |      |      |      |
  3  |  {31}  |  {32}  |  {33}  |
     |______|______|______|
"""
        
        await ctx.send('This game is not finished yet! :3')

def setup(bot):
    bot.add_cog(Games(bot))
