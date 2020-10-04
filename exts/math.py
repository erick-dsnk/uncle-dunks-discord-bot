import discord
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Octal representation of a number command
    @commands.command()
    async def octal(self, ctx, arg):
        chnl = ctx.channel
        
        if arg != None:
            try:
                arg = int(arg)
            except Exception as e:
                print(f"An error occured while handling an octal command: {e}")

            if type(arg) == int:
                await chnl.send("The octal representation of that number is {}.".format(oct(arg)))
            else:
                await chnl.send(f"{arg} is not an integer.")
        
        else:
            await chnl.send(":x: Missing required argument <number>")


    # Binary code of a number command
    @commands.command()
    async def binary(self, ctx, arg):
        chnl = ctx.channel

        if arg != None:
            try:
                arg = int(arg)
            except Exception as e:
                print(f"An error occured while handling a binary command: {e}")


            if type(arg) == int:
                await chnl.send("The binary code of that number is {0:b}".format(arg))
            else:
                await chnl.send(f"{arg} is not an integer.")
            
        else:
            await chnl.send(":x: Missing required argument <number>")


    # Hexadecimal code of a number command
    @commands.command(aliases=["hex"])
    async def hexadecimal(self, ctx, arg):
        chnl = ctx.channel

        if arg != None:
            try:
                arg = int(arg)
            except Exception as e:
                print(f"An error occured while handling a hexadecimal command: {e}")
            

            if type(arg) == int:
                await chnl.send("The hexadecimal code of that number is {}".format(hex(arg)))
            else:
                await chnl.send(f"{arg} is not an integer.")
        
        else:
            await chnl.send(":x: Missing required argument <number>")


def setup(bot):
    bot.add_cog(Math(bot))

