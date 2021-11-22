import discord
import json
import pymongo
import os
from pymongo import MongoClient
from discord.ext import commands

from dotenv import load_dotenv

# Loads the environment variables
load_dotenv()

# Connects to the database cluster
cluster = MongoClient(os.getenv('MongoDB_Connection_URL'))

# The name of the database
db = cluster['PythonBot']

# The name of the collection
collection = db['MessageRankings']


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
    # Counts and stores the number of messages each user has sent to the server
    # within a MongoDB database
    # Guide: https://towardsdatascience.com/creating-a-discord-bot-from-scratch-and-connecting-to-mongodb-828ad1c7c22e
    @commands.Cog.listener()
    async def on_message(self, message):
        query = {'_id': message.author.id}
        # If the current id is different than what is already in the database
        # then we will enter the user ID into the database
        if collection.count_documents(query) == 0:
            # Attibutes to our entry
            post = {'_id': message.author.id, 'messages_sent': 1}
            # Adds the post to the collection
            collection.insert_one(post)
        else:
            # Finds the user that is already in the database
            user = collection.find(query)
            for result in user:
                messages_sent = result['messages_sent']
            # Increments the number of messages sent
            messages_sent = messages_sent + 1
            # Updates pre-existing entries if the user is already in the database
            collection.update_one({'_id': message.author.id},
                                  {'$set': {'messages_sent': messages_sent}})


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
    @commands.command(aliases = ['c'],
                      help = 'Clears the last n number of messages from the channel')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1):
        try:
            await ctx.channel.purge(limit = amount + 1)
        except:
            await ctx.reply('Please only enter numbers greater than 1')
        
    
    # Mutes the member in the server and gives the member a created 'muted' role
    # Only allows those with the 'kick_members' permissions to mute members
    @commands.command(aliases = ['m'], help = 'Mutes a specific member with a muted role')
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member:discord.Member):
        muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted')


    # Unmutes the member in the server and removes the 'muted' role
    # Only allows those with the 'kick_members' permissions to unmute members
    @commands.command(aliases = ['um'], help = 'Unmutes a member and removes their muted rol')
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member:discord.Member):
        muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted')


    # Kicks the member from the server with a reason and DMs the kicked member
    # Only allows those with the 'kick_members' permissions to kick members
    @commands.command(aliases = ['k'], help = 'Kicks the member')
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
    @commands.command(aliases = ['b'], help = 'Bans the member')
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
    @commands.command(aliases = ['ub'], help = 'Unbans the member')
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