import discord
import json
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.errors import BadArgument, CommandError, CommandInvokeError


#----------------------------------------Moderation Commands---------------------------------------


class Moderation(commands.Cog):


    # Initialization that allows us to acces the bot within the cog
    def __init__(self, bot):
        self.bot = bot

    # Reads from the filtered_words.txt file to create a list of filtered words
    filtered_words_file = open('./text_files/filtered_words.txt', 'r')
    filtered_words_list = filtered_words_file.read().splitlines()
    filtered_words_file.close()


    # Correct notation for events
    # Ensures the bot doesn't respond to its own messages
    # Deletes the message if the message contains a word from the list of filtered words
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for word in self.filtered_words_list:
            if word in message.content:
                await message.delete()

        try:
            if message.mentions[0] == self.bot.user:
                with open('prefixes.json', 'r') as f:
                    prefixes = json.load(f)
            
                prefix = prefixes[str(message.guild.id)]
                await message.channel.send(f'The bot command prefix for this server is {prefix}')
        except:
            pass


    # Correct notation for commands
    # Clears the latest 'amount' of messages incremented by one to include the bot's message
    # Only allows those with the 'manage_messages' permissions to clear messages
    @commands.command(aliases = ['c'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1):
        try:
            await ctx.channel.purge(limit = amount + 1)
        except:
            await ctx.reply('Please only enter numbers greater than 1')
        
    
    # Mutes the member in the server and gives the member a created 'muted' role
    # Only allows those with the 'kick_members' permissions to mute members
    @commands.command(aliases = ['m'])
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member:discord.Member):
        muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted')


    # Unmutes the member in the server and removes the 'muted' role
    # Only allows those with the 'kick_members' permissions to unmute members
    @commands.command(aliases = ['um'])
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member:discord.Member):
        muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted')


    # Kicks the member from the server with a reason and DMs the kicked member
    # Only allows those with the 'kick_members' permissions to kick members
    @commands.command(aliases = ['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member, *, reason = 'No reason provided'):
        try:
            await member.kick(reason = reason)
            await ctx.send(f'{member.name} has been kicked from the server because: {reason}')
            await member.send(f'You have been kicked from the server because: {reason}')
        except:
            await ctx.reply('We are unable to process this request at the time')


    # Bans the member from the server with a reason and DMs the banned member
    # Only allows those with the 'kick_members' permissions to ban members
    @commands.command(aliases = ['b'])
    @commands.has_permissions(kick_members = True)
    async def ban(self, ctx, member:discord.Member, *, reason = 'No reason provided'):
        try:
            await member.ban(reason = reason)
            await ctx.send(f'{member.name} has been banned from the server because: {reason}')
            await member.send(f'You have been banned from the server because: {reason}')
        except:
            await ctx.reply('We are unable to process this request at the time')        


    # Unbans the member from the server
    # Only allows those with the 'kick_members' permissions to unban members
    @commands.command(aliases = ['ub'])
    @commands.has_permissions(kick_members = True)
    async def unban(self, ctx, *, member):
        try:
            banned_members = await ctx.guild.bans()
            member_name, member_discord = member.split('#')

            for banned_entry in banned_members:
                user = banned_entry.user

                if (user.name, user.discriminator) == (member_name, member_discord):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{member.name} has been unbanned')
                    return
            await ctx.send(f'{member} was not found.')
        except ValueError:
            await ctx.reply('Please enter in the Username#ID format')


#----------------------------------------Connect Cog to Bot----------------------------------------


# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Moderation(bot))