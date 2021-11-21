import discord
import pandas_datareader as web
# import pandas
# import matplotlib.pyplot as plt
from discord.ext import commands

# A ticker is the stock symbol name
# For example: Apple = AAPL
source = 'yahoo'

#-------------delete in the future-----------------
# https://thecleverprogrammer.com/2021/03/22/pandas-datareader-using-python-tutorial/
# Some same Python pandas and plotting dataframes
# start_date = "2020-01-1"
# end_date = "2020-12-31"
# data = web.DataReader(name="TSLA", data_source='yahoo', start=start_date, end=end_date)
# print(data)
# close = data['Close']
# ax = close.plot(title='Tesla')
# ax.set_xlabel('Date')
# ax.set_ylabel('Close')
# ax.grid()
# plt.show()
#----------------------------------------------------


#----------------------------------------Stock Helper Methods--------------------------------------


# Gets the closing stock price for today
def get_today_stock_price(ticker):
    data = web.DataReader(name = ticker, data_source = source)
    return data['Close'].iloc[-1]


# Gets the stock information from the last five years
def get_stock_information(ticker):
    return web.DataReader(name = ticker, data_source = source)


# Gets the stock information from the start date to the end date
def get_stock_history(ticker, start_date, end_date):
    return web.DataReader(name = ticker, data_source = source,
                          start = start_date, end = end_date)


# print(get_stock_information('AAPL'))


#-------------------------------------------Stock Commands-----------------------------------------


class Stocks(commands.Cog):

    # Initialization that allows us to acces the bot within the cog
    def __init__(self, bot):
        self.bot = bot


    # Displays all of the information on that stock in an embed
    @commands.command(aliases = ['spt'],
                      help = 'Shows the closing price of the stock for the today')
    async def stockpricetoday(self, ctx, *, tickers):
        stocks = tickers.split(' ')
        prices = ''

        for stock in stocks:
            stock_name = f'{stock.upper():8}'
            prices += stock_name
            try:
                price = get_today_stock_price(stock)
                prices += f'{price:8}' + '\n'
            except:
                prices += 'This stock does not exist\n'

        embed = discord.Embed(title = 'Today\'s Closing Stock Prices', description = prices, color = discord.Color.red())
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.display_name}')
        await ctx.send(embed = embed)


#----------------------------------------Connect Cog to Bot----------------------------------------


# Setup that allows us to connect the cog to the bot
def setup(bot):
    bot.add_cog(Stocks(bot))