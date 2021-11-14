import discord
import asyncpraw
from discord.ext import commands


#-----------------------------------------Reddit Commands------------------------------------------


class Reddit(commands.Cog):


    # Initialization that allows us to access the bot within the cog
    def __init__(self, bot):
        self.bot = bot


    # Command that pulls the top number of posts for that day in a specific subreddit community
    @commands.command(aliases = ['rdt', 'r'])
    async def reddit(self, ctx, sub = 'csmajors', num = 5):

        # Initializes the Python Reddit API Wrapper
        reddit = asyncpraw.Reddit('PythonBot', config_interpolation = 'basic')

        # Prints the user agent
        # print(reddit.config.user_agent)

        # Changes to read-only mode
        reddit.read_only = True

        # Gets the subreddit
        subreddit = await reddit.subreddit(sub)

        # Empty list for posts in the subreddit
        posts = []

        # Gets the 'num' number of hottest posts
        hot = subreddit.hot(limit = num)

        # Adds the submissions into the 'posts' list
        async for submission in hot:
            posts.append(submission)
        
        for post in posts:
            title = post.title
            permalink = post.permalink
            upvotes = post.score
            ratio = post.upvote_ratio * 100
            comments = post.num_comments

            # Link of the image associated with the post
            url = post.url
            embed = discord.Embed(title = title,
                                  description = f'https://www.reddit.com{permalink}',
                                  timestamp = ctx.message.created_at,
                                  url = url,
                                  color = discord.Color.red())
            # Shows the image associated with the post
            embed.set_image(url = url)
            embed.add_field(name = 'Upvotes 👍🏻', value = upvotes, inline = True)
            embed.add_field(name = 'Upvote Ratio ⬆️ ⬇️', value = f'{float(ratio):g}%')
            embed.add_field(name = 'Comments 💬', value = comments, inline = True)
            embed.set_footer(text = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)

        # Closes the client session
        await reddit.close()


#----------------------------------------Connect Cog to Bot----------------------------------------


# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Reddit(bot))