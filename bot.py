import discord
import os
import json
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionNotLoaded
from dotenv import load_dotenv

# Loads the environment variables
load_dotenv()

#-------------------------------Server-Specific Custom Prefix Command------------------------------

# Gets the bot command prefix from the .json file
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    return prefixes[str(message.guild.id)]

# The bot's command prefix
bot = commands.Bot(command_prefix = get_prefix)

# Sets the default server-specific prefix for the bot command on joining the server
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    
    # Default prefix
    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file)

# Sets the prefix for the bot commands
# Only allows those with administrator permissions to change the prefix
@bot.command(aliases = ['changeprefix'])
@commands.has_permissions(administrator = True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    
    # Saves the server specific prefix into the json folder
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file)
    
    await ctx.reply(f'The command prefix is now {prefix}')

#-------------------------------------------Bot Start Up-------------------------------------------

# Stores the server ID and the respective set prefix command for the server in the .json file
# Prints a message to the console if the bot successfully connects to the Discord server
@bot.event
async def on_ready():
    for guild in bot.guilds:
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)
    
        prefixes[str(guild.id)] = '!'

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file)
    print(f'{bot.user} has connected to {guild.name}!')

#--------------------------------------Loading/Unloading Cogs--------------------------------------

# Loads the cog .py file from the 'cogs' folder
@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
        await ctx.reply(f'Loaded the {extension} extension')
    except ExtensionAlreadyLoaded:
        await ctx.reply('The extension has already been loaded')

# Unloads the cog .py file from the 'cogs' folder
@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.reply(f'Unloaded the {extension} extension')
    except ExtensionNotLoaded:
        await ctx.reply('The extension is already unloaded')

# Looks for the appropriate cog .py file within the 'cogs' folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # Splicing to get rid of the '.py' at the end of the file name
        bot.load_extension(f'cogs.{filename[:-3]}')

#------------------------------------------Error Handling------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.ExtensionNotLoaded):
        await ctx.reply('The extension is already unloaded')
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.reply('The extension has already been loaded')
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, ExtensionNotFound):
            await ctx.reply('The extension could not be found')
        elif isinstance(error.original, Forbidden):
            await ctx.reply('You are missing the permissions to do this')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply('That command could not be found')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply('The member could not be found')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Please enter the missing arguments')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply('You do not have the required permissions to do that')
    else:
        raise error

#-------------------------------------------Bot Start Up-------------------------------------------

# Runs the bot with the appropriate Discord bot token
bot.run(os.getenv('Discord_Bot_Token'))