import discord
from discord.ext import commands


#-----------------------------------------General Commands-----------------------------------------


class General(commands.Cog):


    # Initialization that allows us to access the bot within the cog
    def __init__(self, bot):
        self.bot = bot


    # Sends a general greeting
    @commands.command()
    async def greet(self, ctx, name = ''):
        if (name == ''):
            await ctx.send('Hey there!')
        else:
            await ctx.send(f'Hey {name}!')
    

    # Adds numbers together using *args
    @commands.command()
    async def add(self, ctx, *values):
        try:
            sum = 0
            for num in values:
                sum += int(num)
            await ctx.reply(sum)
        except ValueError:
            await ctx.reply('Please enter integers only')


    # # Just a test subroutine to show alternative commands to the subroutine signature name
    # @commands.command(name = 'alternative_name')
    # async def testing(self, ctx, num1:int, num2:int):
    #     await ctx.reply(num1 + num2)


#----------------------------------------Connect Cog to Bot----------------------------------------


# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(General(bot))