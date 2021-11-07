import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = commands.Bot(command_prefix='!')

# Sends a message to the console if the bot successfully connects to Discord
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

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


# sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

# starter_encouragements = [
#     "Cheer up!",
#     "Hang in there!",
#     "You are awesome!"
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
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + " -" + json_data[0]['a']
#     return quote

# # Runs the bot with the bot token (the bot's token is like its password)
# client.run(token)