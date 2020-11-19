import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from exts.database import economy_collection
import random


class Economy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command()
    async def work(self, ctx: Context):
        guild_data = economy_collection.find_one({"_id": ctx.message.guild.id})

        members_data = guild_data['members']

        for member in members_data:
            if member['id'] == ctx.message.author.id:
                amount = random.randint(50, 200)
                member['money'] += amount

                break
            
            else:
                pass
        
        economy_collection.find_one_and_update({"_id": ctx.message.guild.id}, {"$set": {"members": members_data}})
        
        await ctx.send(f'You earned {amount} coins!')
    
    @work.error
    async def work_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You're on cooldown! You can only use the `work` command every 30 minutes!")


    @commands.command()
    async def balance(self, ctx: Context, user: discord.Member = None):
        if user == None:
            user = ctx.message.author
        
        members_data = economy_collection.find_one({"_id": ctx.message.guild.id})['members']

        for member in members_data:
            if member['id'] == user.id:
                embed = discord.Embed(
                    title=f"**{user.name}#{user.discriminator}'s** balance in **{ctx.guild.name}**",
                    description=f"Cash: `{member['money']} coins`\nBank: `Coming Soon`",
                    colour=discord.Color.blurple()
                )

                embed.set_footer(f"Requested by {user.mention}")

                await ctx.send(embed=embed)

                break
            
            else: pass

def setup(bot):
    bot.add_cog(Economy(bot))
