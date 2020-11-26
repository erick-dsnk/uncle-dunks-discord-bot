import random
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from random import choice, randint


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
        Play a game of Tic Tac Toe against Uncle Dunk!
        '''
        finished = False

        table = """
```
     ______________________
     |      |      |      |
     |  A1  |  A2  |  A3  |
     |______|______|______|
     |      |      |      |
     |  B1  |  B2  |  B3  |
     |______|______|______|
     |      |      |      |
     |  C1  |  C2  |  C3  |
     |______|______|______|
```
"""
        
        message = await ctx.send(table)

        available_choices = [
            'A1',
            'A2',
            'A3',
            'B1',
            'B2',
            'B3',
            'C1',
            'C2',
            'C3'
        ]

        table_matrix = [
            ['A1', 'A2', 'A3'],
            ['B1', 'B2', 'B3'],
            ['C1', 'C2', 'C3']
        ]

        while not finished:
            choice = await self.bot.wait_for('message', check = lambda msg: msg.author == ctx.author)

            

            if not choice.content in available_choices:
                await ctx.send("That's not a valid choice!")
            
            elif choice.content == 'stop':
                break

            if len(available_choices) != 1:
                for c in available_choices:
                    if c == choice.content:
                        del available_choices[available_choices.index(c)]
                
                bot_choice = random.choice(available_choices)

                for c in available_choices:
                    if c == bot_choice:
                        del available_choices[available_choices.index(c)]

                table = table.replace(choice.content, "X ").replace(bot_choice, "O ")

                if choice.content == 'A1':
                    table_matrix[0][0] = 'X '
                
                elif choice.content == 'A2':
                    table_matrix[0][1] = 'X '
                
                elif choice.content == 'A3':
                    table_matrix[0][2] = 'X '
                
                elif choice.content == 'B1':
                    table_matrix[1][0] = 'X '

                elif choice.content == 'B2':
                    table_matrix[1][1] = 'X '

                elif choice.content == 'B3':
                    table_matrix[1][2] = 'X '

                elif choice.content == 'C1':
                    table_matrix[2][0] = 'X '

                elif choice.content == 'C2':
                    table_matrix[2][1] = 'X '

                elif choice.content == 'C3':
                    table_matrix[2][2] = 'X '



                if bot_choice == 'A1':
                    table_matrix[0][0] = 'O '

                elif bot_choice == 'A2':
                    table_matrix[0][1] = 'O '

                elif bot_choice == 'A3':
                    table_matrix[0][2] = 'O '

                elif bot_choice == 'B1':
                    table_matrix[1][0] = 'O '

                elif bot_choice == 'B2':
                    table_matrix[1][1] = 'O '

                elif bot_choice == 'B3':
                    table_matrix[1][2] = 'O '

                elif bot_choice == 'C1':
                    table_matrix[2][0] = 'O '

                elif bot_choice == 'C2':
                    table_matrix[2][1] = 'O '

                elif bot_choice == 'C3':
                    table_matrix[2][2] = 'O '

            
            else:
                for c in available_choices:
                    if c == choice.content:
                        del available_choices[available_choices.index(c)]

                table = table.replace(choice.content, "X ")

                if choice.content == 'A1':
                    table_matrix[0][0] = 'X '

                elif choice.content == 'A2':
                    table_matrix[0][1] = 'X '

                elif choice.content == 'A3':
                    table_matrix[0][2] = 'X '

                elif choice.content == 'B1':
                    table_matrix[1][0] = 'X '

                elif choice.content == 'B2':
                    table_matrix[1][1] = 'X '

                elif choice.content == 'B3':
                    table_matrix[1][2] = 'X '

                elif choice.content == 'C1':
                    table_matrix[2][0] = 'X '

                elif choice.content == 'C2':
                    table_matrix[2][1] = 'X '

                elif choice.content == 'C3':
                    table_matrix[2][2] = 'X '

            await message.edit(
                content=table
            )

            if (
                (table_matrix[0][0] == 'X ' and table_matrix[0][1] == 'X ' and table_matrix[0][2] == 'X ')
                or
                (table_matrix[1][0] == 'X ' and table_matrix[1][1] == 'X ' and table_matrix[1][2] == 'X ')
                or
                (table_matrix[2][0] == 'X ' and table_matrix[2][1] == 'X ' and table_matrix[2][2] == 'X ')
                or
                (table_matrix[0][0] == 'X ' and table_matrix[1][0] == 'X ' and table_matrix[2][0] == 'X ')
                or
                (table_matrix[0][1] == 'X ' and table_matrix[1][1] == 'X ' and table_matrix[2][1] == 'X ')
                or
                (table_matrix[0][2] == 'X ' and table_matrix[1][2] == 'X ' and table_matrix[2][2] == 'X ')
            ):
                await ctx.send("You won!")

                break
            
            elif (
                (table_matrix[0][0] == 'O ' and table_matrix[0][1] == 'O ' and table_matrix[0][2] == 'O ')
                or
                (table_matrix[1][0] == 'O ' and table_matrix[1][1] == 'O ' and table_matrix[1][2] == 'O ')
                or
                (table_matrix[2][0] == 'O ' and table_matrix[2][1] == 'O ' and table_matrix[2][2] == 'O ')
                or
                (table_matrix[0][0] == 'O ' and table_matrix[1][0] == 'O ' and table_matrix[2][0] == 'O ')
                or
                (table_matrix[0][1] == 'O ' and table_matrix[1][1] == 'O ' and table_matrix[2][1] == 'O ')
                or
                (table_matrix[0][2] == 'O ' and table_matrix[1][2] == 'O ' and table_matrix[2][2] == 'O ')
            ):
                await ctx.send("You lost! Good luck next time!")

                break

            else:
                pass


    @commands.command()
    async def roll(self, ctx: Context, bet: int):
        '''
        Roll a dice!
        '''
        bot_choice = randint(1, 6)

        if type(bet) != int:
            await ctx.send(":x: That's not a number!")
            return

        if bet == bot_choice:
            statement = "You were right!"
        
        else:
            statement = "Better luck next time!"

        embed = discord.Embed(
            title=":dice: Roll!",
            description=f"Your bet: `{bet}`\nOutcome: `{bot_choice}`\n\n**{statement}**"
        )

        await ctx.send(embed=embed)
    

    @commands.command()
    async def flip(self, ctx: Context, bet: str):
        '''
        Flip a coin!
        `heads` or `tails`
        '''
        choices = ['heads', 'tails']

        if bet in choices:
            bot_choice = random.choice(choices)

            if bet == bot_choice:
                final_statement = 'You win!'
            
            else:
                final_statement = 'You lose!'

            await ctx.send(f"{bot_choice.title()}!")

        else:
            await ctx.send("That's not a valid choice!")


def setup(bot):
    bot.add_cog(Games(bot))
