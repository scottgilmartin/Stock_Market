from Stock_Market import Stock, Trade, Market
from datetime import datetime, timedelta
import random

# A simple example in which random stock trades are performed and stored in a stock market class.
# A list of recent trades is printed in chronological order, along with some numerical data.

pop_stock = Stock('POP', 'common', 8, 100)
gin_stock = Stock('GIN', 'preferred', 8, 100, 0.02)  # create the stocks to be traded

market = Market()  # create the market

# generate some random trades

pop_buys = [market.market_trade(pop_stock, datetime.utcnow()-timedelta(minutes=random.randrange(20)),
                                random.randrange(1000), 'buy', random.randrange(10,100)) for _ in range(5)]

pop_sells = [market.market_trade(pop_stock, datetime.utcnow()-timedelta(minutes=random.randrange(20)),
                                 random.randrange(1000), 'sell', random.randrange(10,100)) for _ in range(5)]

gin_buys = [market.market_trade(gin_stock, datetime.utcnow()-timedelta(minutes=random.randrange(20)),
                                random.randrange(1000), 'buy', random.randrange(10,100)) for _ in range(5)]

gin_sells = [market.market_trade(gin_stock, datetime.utcnow()-timedelta(minutes=random.randrange(20)),
                                 random.randrange(1000), 'sell', random.randrange(10,100)) for _ in range(5)]


print(market.stocks)  # print stocks which have been traded in the market 
print(market.latest_trades())  # print recent trades in the market

for stock in market.stocks:
    print('Stock: ' + str(stock))
    print('Dividend Yield: ' + str(stock.dividend_yield(50)))
    print('P/E Ratio: ' + str(stock.p_e_ratio(50)))
    print('Volume Weighted Price: ' + str(market.vol_weighted_stock_price(stock)))

print('All Share Index: ' + str(market.all_share_index()))
