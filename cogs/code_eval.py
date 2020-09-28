import discord
from discord.ext import commands
import subprocess
from subprocess import PIPE
import os


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=['code', 'codeeval', 'evalcode'])
    async def e(self, ctx, *, code_block):
        with open(f"{ctx.guild.id}.py", 'w') as f:
            f.write(code_block.strip('`'))
        
        command = subprocess.run(f'python {ctx.guild.id}.py', stdout=PIPE, stderr=PIPE)

        await ctx.send(
            f'```\n{command.stdout.decode()}\n```'
        )

        os.remove(f'{ctx.guild.id}.py')


def setup(bot):
    bot.add_cog(Eval(bot))