import discord
from discord.ext import commands

#---------------------------------------General Embed Commands-------------------------------------

class Embed(commands.Cog):

    # Initialization that allows us to acces the bot within the cog
    def __init__(self, bot):
        self.bot = bot
    
    # Bot command that shows info about the member including their name, ID, avatar, and join date
    # Displays the info in an embed and shows who requested the command
    @commands.command(aliases = ['user', 'info'])
    @commands.has_permissions(kick_members = True)
    async def whois(self, ctx, member:discord.Member):
        embed = discord.Embed(title = member.name, description = member.mention, color = discord.Color.red())
        embed.add_field(name = 'ID', value = member.id, inline = True)
        embed.add_field(name = 'Joined Server', value = member.joined_at, inline = True)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
        await ctx.send(embed = embed)

    # Creates a poll given two options separated by 'or'
    # Limited to only two options (so far)
    @commands.command()
    async def poll(self, ctx, *, message):
        channel = ctx.channel
        split = message.split('?')
        question = split[0] + '?'

        try:
            numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            options = split[1].split('or')
            
            text = ''
            for o in range(len(options)):
                text += f'{numbers[o]} {options[o]}'
                text += '\n'

            embed = discord.Embed(title = question, description = text, colour = discord.Colour.red())
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Poll by {ctx.author.name}')
            poll_message = await channel.send(embed = embed)
            await ctx.message.delete()
            for o in range(len(options)):
                await poll_message.add_reaction(f'{numbers[o]}')
        except ValueError:
            await ctx.reply('Please enter a question ending in \'?\' and between 2 to 10 options separated by \'or\'')
        except:
            await ctx.reply('Please enter a question ending in \'?\' and between 2 to 10 options separated by \'or\'')

#----------------------------------------Connect Cog to Bot----------------------------------------

# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Embed(bot))