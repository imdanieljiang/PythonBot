import discord
from discord.ext import commands

#------------------------------------------Rules Commands------------------------------------------

class Rules(commands.Cog):

    # Initialization that allows us to access the bot within the cog
    def __init__(self, bot):
        self.bot = bot
    
    # Reads from the 'rules.txt' file and make a list of rules
    rules_file = open('./text_files/rules.txt', 'r')
    rules_list = rules_file.readlines()
    # Uncomment this to exclude '\n' characters
    # rules_list = rules_file.read().splitlines()
    rules_file.close()

    # Sends the list of rules to the Discord server separated by newline characters '\n'
    @commands.command()
    async def rules(self, ctx):
        await ctx.send('\n'.join(self.rules_list))
    
    # Sends a specific rule to the Discord server
    @commands.command()
    async def rule(self, ctx, *, number):
        if int(number) >= 1 and int(number) <= len(self.rules_list) - 1:
            await ctx.send(self.rules_list[int(number)])
        else:
            await ctx.send(f'Rule {number} doesn\'t exist')

#----------------------------------------Connect Cog to Bot----------------------------------------

# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Rules(bot))