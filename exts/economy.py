import discord
from discord import member
from discord.ext import commands
from discord.ext.commands import Cog, Context, Bot
from exts.database import economy_collection
import random


def convert_to_time(seconds):
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return f"{hours} hours, {minutes} minutes, {seconds} seconds"


class Economy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @commands.cooldown(1, 1800, commands.BucketType.member)
    @commands.command()
    async def work(self, ctx: Context):
        '''
        Earn your money the honest way! You can get between 50 and 300 dunk dollars working! 
        You can only work once every 30 minutes.
        '''
        guild_data = economy_collection.find_one({"_id": ctx.message.guild.id})

        members_data = guild_data['members']

        for member in members_data:
            if member['id'] == ctx.message.author.id:
                amount = random.randint(50, 300)
                member['money'] += amount

                break
            
            else:
                pass
        
        economy_collection.find_one_and_update({"_id": ctx.message.guild.id}, {"$set": {"members": members_data}})
        
        embed = discord.Embed(
            title=":office: Job",
            description=f"You earned {amount} coins!",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)
    
    @work.error
    async def work_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @commands.cooldown(1, 10800, type=commands.BucketType.member)
    @commands.command()
    async def rob(self, ctx: Context, user: discord.Member):
        '''
        Take a risk and mug someone... You can lose a lot of money if you get caught... But you can also *win* a lot of money if you get away with it!
        You can only rob someone every 3 hours.
        Rewards are between 300 and 1000 dunk dollars. Fines are between 100 and 200 dunk dollars.
        '''
        members_data = economy_collection.find_one({"_id": ctx.guild.id})['members']

        robber = ctx.author
        victim = user

        success = random.random() * 100

        amount = random.randint(300, 1000)
        fine = random.randint(100, 200)

        if success >= 30.0:
            for member in members_data:
                if member['id'] == robber.id:
                    if member['money'] < fine:
                        member['money'] = 0
                    
                    else:
                        member['money'] -= fine
                
                elif member['id'] == victim.id:
                    member['money'] += fine * 2
                
                else:
                    pass
            
            embed = discord.Embed(
                title="Busted!",
                description=f"You tried robbing {victim.mention} but you got caught and you lost {amount} coins!",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)

                
        else:
            for member in members_data:
                if member['id'] == robber.id:
                    member['money'] += amount

                elif member['id'] == victim.id:
                    if member['money'] < (amount / 2):
                        member['money'] = 0
                    
                    else:
                        member['money'] -= (amount / 2)
                else:
                    pass
            
            embed = discord.Embed(
                title="Success!",
                description=f"You managed to get away with robbing {victim.mention} and earned {amount}!",
                color=discord.Color.green()
            )

            await ctx.send(embed=embed)
                
        economy_collection.update_one({"_id": ctx.guild.id}, {"$set": {"members": members_data}})

    @rob.error
    async def rob_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @commands.cooldown(1, 86400, commands.BucketType.member)
    @commands.command()
    async def daily(self, ctx: Context):
        '''
        Collect your daily 500 dunk dollar bonus!
        '''
        members = economy_collection.find_one({"_id": ctx.guild.id})['members']

        for member in members:
            if member['id'] == ctx.author.id:
                member['money'] += 500
        
        embed = discord.Embed(
            title="**Daily bonus!**",
            description=":white_check_mark: Successfully claimed your daily `500` dunk dollars bonus!",
            color=discord.Color.green()
        )

        economy_collection.find_one_and_update({"_id": ctx.guild.id}, {"$set": {"members": members}})

        await ctx.send(embed=embed)


    @daily.error
    async def daily_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @commands.command()
    async def balance(self, ctx: Context, user: discord.Member = None):
        '''
        Check your account balance.
        '''
        if user == None:
            user = ctx.message.author
        
        members_data = economy_collection.find_one({"_id": ctx.message.guild.id})['members']

        for member in members_data:
            if member['id'] == user.id:
                embed = discord.Embed(
                    title=":bank: Bank of Dunkville",
                    description=f"Bank statement of {user.name}#{user.discriminator}",
                    color=discord.Color.blurple()
                )

                embed.add_field(
                    name=":moneybag: Cash",
                    value=f"`{member['money']}$`"
                )

                embed.add_field(
                    name=":bank: Account",
                    value=f"`{member['bank']}$`"
                )

                embed.set_footer(text=f"Requested by {user.name}#{user.discriminator}")

                await ctx.send(embed=embed)

                break
            
            else: pass
    

    @commands.command()
    async def deposit(self, ctx: Context, amount) -> None:
        '''
        Deposit your money in the bank to be protected from thiefs!
        You can use `all` as the amount to deposit all of your cash in the bank.
        '''
        members_data = economy_collection.find_one({"_id": ctx.guild.id})['members']
        
        final = None

        for member in members_data:
            if member['id'] == ctx.message.author.id:
                final = member

                if amount == 'all':
                    amount = member['money']

                    member['bank'] += amount
                    member['money'] -= amount

                    break
            
                elif int(amount) <= member['money']:
                    member['money'] -= int(amount)
                    member['bank'] += int(amount)

                    break
                
                else:
                    amount = member['money']
                    
                    member['money'] -= amount
                    member['bank'] += amount

                    break
            
            else:
                pass
        
        economy_collection.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"members": members_data}}
        )

        embed = discord.Embed(
            title=":bank: Bank of Dunkville",
            description=f"Succesfully deposited {amount}$ in your bank account.",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name=":moneybag: Cash",
            value=f"`{final['money']}$`"
        )

        embed.add_field(
            name=":bank: Account",
            value=f"`{final['bank']}$`"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
