import discord
import os
import asyncpraw
import random
from discord.ext import commands
from dotenv import load_dotenv

# Loads the environment variables
load_dotenv()

# Initializes the Python Reddit API Wrapper
reddit = asyncpraw.Reddit(client_id = os.getenv('Reddit_Client_ID'),
                     client_secret = os.getenv('Reddit_Client_Secret'),
                     username = os.getenv('Reddit_Username'),
                     password = os.getenv('Reddit_Password'),
                     user_agent = 'thiscanbeanything',
                     check_for_async = False


# subreddit = reddit.subreddit('memes')
# top = subreddit.top(limit = 10)
# all_submissions = []
# for submission in top:
#     all_subs.append(submission)
#     print(submission.title)


#-----------------------------------------Reddit Commands------------------------------------------


class Reddit(commands.Cog):


    # Initialization that allows us to access the bot within the cog
    def __init__(self, bot):
        self.bot = bot


    # Command that pulls the top number of posts for that day in a specific subreddit community
    @commands.command(aliases = ['rt', 'rtop'])
    async def reddittop(self, ctx, topnum = '10', sub = 'csMajors'):
        subreddit = reddit.subreddit(sub)
        top_posts = subreddit.top('day')
        all_posts = []

        for submission in top_posts:
            all_posts.append(submission)
        
        random_sub = random.choice(all_posts)

        name = random_sub.title
        url = random_sub.url

        print(name)
        print(url)

        embed = discord.Embed(title = name, description = url, color = discord.Color.red())
        # embed.add

        # embed.set_image(url = url)

        await ctx.send(embed = embed)



#----------------------------------------Connect Cog to Bot----------------------------------------


# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Reddit(bot))