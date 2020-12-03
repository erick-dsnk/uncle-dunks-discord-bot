import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot


class Info(Cog):
		def __init__(self, bot: Bot):
			self.bot = bot

		@commands.command()
		async def help(self, ctx: Context, category: str = ""):
			if category == "":
				embed = discord.Embed(
					 title="Commands help",
					 description="""
**Categories:**
 - `entertainment`
 - `games`
 - `math`
 - `utility`
 - `moderation`

Use `-help <category>` to get a list of commands inside of the specific categories. **Don't include the brackets!**
""",
					 color=discord.Color.blurple()
				)
		  
			elif category == "entertainment":
				embed = discord.Embed(
					title="Entertainment Commands",
					description="""
 - `-meme`
	 *It sends you a hot meme off Reddit!*

 - `-joke`
	 *Tells you a top-notch joke.*

 - `-doggo`
	 *Sends you a picture of a cute doggo :3*

 - `-8ball <question>`
	 *Shake the Magic 8 Ball and get an answer to your question*
	 *Usage: `-8ball Am I a good cookie?`*
""",
					color=discord.Color.blurple()
				)
		  
			elif category == "games":
				embed = discord.Embed(
					title="Game commands",
					description="""
 - `-rps <choice>`
	 *Play a good game of Rock, Paper, Scissors with Uncle Dunk!*
	 *Choices: `rock`, `paper`, `scissors`*

 - `-tictactoe`
	 *Play a game of Tic Tac Toe against Uncle Dunk! (WIP)*
""",
					color=discord.Color.blurple()
				)
		  
			elif category == "math":
				embed = discord.Embed(
					title="Math commands",
					description="""
 - `-binary <number>`
	 *Calculate the binary representation of this number*

 - `-hexadecimal <number>`
	 *Calculate the hexadecimal representation of this number*

 - `-octal <number>`
	 *Calculate the octal representation of this number*
""",
					color=discord.Color.blurple()
				)
		  
			elif category == "moderation":
				embed = discord.Embed(
					title="Moderation commands",
					description="""
 - `-kick <member> [reason]`
	 *Kick a member from the server.*
	 *Usage: `-kick @BadCookie#0001 You are a bad cookie >:(`*

 - `-ban <member> [reason]`
	 *Ban a member from the server.*
	 *Usage: `-ban @BadCookie#0001 You are a VERY bad cookie >:(`*

 - `-mute <member> [duration]`
	 *Restrict a member from sending messages*
	 *Duration is an optional argument and it will mute the member for 15 minutes if none is given.*
	 *The duration argument can be passed in seconds (`50s`), minutes (`20m`), hours (`2h`) or days (`7d`).*

 - `-unmute <member>`
	 *It gives the member ability to send messages again.*

 - `-vcmute <member> [duration]`
	 *Restrict a member speaking in voice channels*
	 *Duration is an optional argument and it will mute the member for 15 minutes if none is given.*
	 *The duration argument can be passed in seconds (`50s`), minutes (`20m`), hours (`2h`) or days (`7d`).*

 - `-vcunmute <member>`
	 *It gives the member ability to speak in voice channels again.*
""",
					color=discord.Color.blurple()
				)

			elif category == "utility":
				embed = discord.Embed(
					title="Utility commands",
					description="""
 - `-news [topic]`
	 *Get top 3 headlines from the most trusted news sources!*

 - `-corona <location>`
	 *Get information about the latest COVID-19 pandemic situation in a city or country.*

 - `-wikisearch <query>`
	 *Search Wikipedia about a certain topic.*

 - `-weather <location>`
	 *Sends you the latest weather forecast in a city or country.*

 - `-avatar [member]`
	 *Like a person's profile picture? You can now get it with this command!*

 - `-info`
	 *Get information about the bot and its status.*

 - `-userinfo [member]`
	 *Get information about a certain user!*

 - `-serverinfo`
	 *Get information about the server the command was used in.*

 - `-source`
	 *Sends the link to the GitHub repository where the source code is kept.*
""",
					color=discord.Color.blurple()
				)
		  
			else:
				embed = discord.Embed(
					title="Oops!",
					description="Sorry, there's no category with that name!",
					color=discord.Color.red()
				)

			await ctx.send(embed=embed)


def setup(bot: Bot):
	bot.add_cog(Info(bot))
