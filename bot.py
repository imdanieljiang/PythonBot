import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = commands.Bot(command_prefix = '!')

# Sends a message to the console if the bot successfully connects to Discord
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#--------------------------------------------------------------------------------------------------

# Reading from the rules.txt file to make a list of rules
rules_file = open('rules.txt', 'r')
list_of_rules = rules_file.readlines()
# Uncomment this to exclude \n characters
# list_of_rules = rules_file.read().splitlines()
rules_file.close()

# Sends the list of rules for the Discord server separated by newline characters '\n'
@bot.command()
async def rules(ctx):
    await ctx.send('\n'.join(list_of_rules))

# Sends a specific rule to the Discord server
@bot.command()
async def rule(ctx, *, num):
    if (int(num) >= 1 and int(num) <= len(list_of_rules) - 1):
        await ctx.send(list_of_rules[int(num)])
    else:
        await ctx.send('Rule ' + num + ' doesn\'t exist')

#--------------------------------------------------------------------------------------------------

# Sends a general greeting or a personal one to a specified name or user
@bot.command()
async def greet(ctx, name=''):
    if (name == ''):
        await ctx.send('Hi there!')
    else:
        await ctx.send('Hi ' + name + '!')

# Simply adds two numbers together
@bot.command()
async def add(ctx, num1:int, num2:int):
    await ctx.reply(num1 + num2)

# Just a test subroutine to show alternative commands to the subroutine signature name
@bot.command(name = 'alternative_name')
async def testing(ctx, num1:int, num2:int):
    await ctx.reply(num1 + num2)

#------------------------------------Moderation Commands-------------------------------------------

# Clears the latest 'amount' of messages incremented by one to include the bot's message
# Only allows those with the permissions to delete messages
@bot.command(aliases = ['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)

# Mutes the member in the server
# Gives the member a created 'Muted' role
@bot.command(aliases = ['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member:discord.Member):
    muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
    await member.add_roles(muted_role)
    await ctx.send(member.mention + ' has been muted')

# Unmutes the member in the server
# Removes the 'Muted' role form the member
@bot.command(aliases = ['um'])
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member:discord.Member):
    muted_role = ctx.guild.get_role(907114788352569394) # 'Muted' role ID
    await member.remove_roles(muted_role)
    await ctx.send(member.mention + ' has been unmuted')

# Kicks the member from the server
# Only allows those with the permissions to kick members
# Provides a reason and notifies the kicked member in DMs
@bot.command(aliases = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member:discord.Member, *, reason = 'No reason provided'):
    await member.send('You have been kicked from the server because: ' + reason)
    await member.kick(reason = reason)

# Bans the member from the server
# Only allows those with the permissions to ban members
# Provides a reason and notifies the banned member in DMs
@bot.command(aliases = ['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member:discord.Member, *, reason = 'No reason provided'):
    await ctx.send(member.name + ' has been banned from the server because: ' + reason)
    await member.send('You have been banned from the server because: ' + reason)
    await member.ban(reason = reason)

# Unbans the member from the server
# Only allows those with permissions to unban members
# Unbans the person using their Discord ID: Name#0000
@bot.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_people = await ctx.guild.bans()
    member_name, member_discord = member.split('#')

    for banned_entry in banned_people:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_discord):
            await ctx.guild.unban(user)
            await ctx.send(member_name + ' has been unbanned')
            return
    await ctx.send(member + ' was not found')

#------------------------------------Discord Bot Start Up------------------------------------------

# Runs the bot with the appropriate Discord bot token
bot.run(getenv('Discord_Bot_Token'))







# import os
# import requests # Allows our code to make HTTP requests to get data from APIs
# import json # The API returns JSON so we have to import the JSON module
# import random
# from dotenv import load_dotenv

# # Allows you to access environment variables from the environment (.env) file
# load_dotenv()
# token = os.environ['Discord_Bot_Token']

# client = discord.Client()


# sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

# starter_encouragements = [
#     'Cheer up!',
#     'Hang in there!',
#     'You are awesome!'
# ]


# # Login message from the bot
# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')

# # The bot will complete actions given specific message commands
# @client.event
# async def on_message(message):
#     # To ensure the bot doesn't respond to its own messages
#     if message.author == client.user:
#         return

#     msg = message.content

#     if msg.startswith('$hello'):
#         await message.channel.send('Hello!')

#     if msg == 'ping':
#         await message.channel.send('pong')

#     if msg.startswith('$inspire'):
#         quote = get_quote()
#         await message.channel.send(quote)

#     if any(word in msg for word in sad_words):
#         await message.channel.send(random.choice(starter_encouragements))

# # Gets a quote from the zenquotes API
# def get_quote():
#     response = requests.get('https://zenquotes.io/api/random')
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + ' -' + json_data[0]['a']
#     return quote

# # Runs the bot with the bot token (the bot's token is like its password)
# client.run(token)