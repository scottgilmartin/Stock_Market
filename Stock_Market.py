from datetime import datetime
import functools 
import operator


class Stock:
    """A class object representing a particular stock.

    Attributes:
        symbol: (str): A three character string representing the stock or company.
        stock_type: (str): The type of stock; either common or preferred.
        last_dividend: (float): The last dividend of the stock.
        par_value: (float): The par value of the stock.
        fixed_dividend: (float or None): The fixed dividend of the stock. (None for common stocks)
        
    """
    
    def __init__(self, symbol, stock_type, last_dividend, par_value, fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.fixed_dividend = fixed_dividend 
        
    def __repr__(self):
        return self.symbol

    def dividend_yield(self, price):
        """The dividend yield of a stock for a given price.

        Args:
            price: (float): The current price of the stock in pennies.

        Returns:
            return: (float): The dividend yield, returns 0 if the current price is 0.
            

        """
        if price == 0:
            return 0
    
        elif self.stock_type == 'common':
            return self.last_dividend/price
        
        elif self.stock_type == 'preferred':
            if self.fixed_dividend is None:
                print('No fixed dividend')
                return 0
            else:
                return (self.fixed_dividend * self.par_value) / price
       
    def p_e_ratio(self, price):
        """The P/E ratio of a stock for a given price.

        Args:
            price: (float): The current price of the stock in pennies.

        Returns:
            return: (float): The P/E ratio, returns 0 if dividend yield is 0.
            

        """
        try:
            return price/self.dividend_yield(price)
        except ZeroDivisionError:
            print('Undefined ratio for zero earnings')
            return 0
        
   
class Trade:
    """A class object representing a trade instance of a particular stock.

    Attributes:
        stock: (Stock obj): The stock being traded.
        trade_time: (datetime obj): The time at which the trade takes place.
        trade quantity: (int): The number of stocks being traded
        trade_direction: (str): The direction of trade; either 'buy' or 'sell'.
        trade_price: (float): the price at which the stock is being traded.
        
    """

    def __init__(self, stock, trade_time, trade_quantity, trade_direction, trade_price):
        self.stock = stock
        self.trade_time = trade_time
        self.trade_quantity = trade_quantity
        self.trade_direction = trade_direction
        if trade_price >= 0:
            self.trade_price = trade_price
        else:
            raise ValueError('Negative price')
        
    def __repr__(self):
        return str(self.stock.symbol + ' ' + str(self.trade_time) + ' ' + str(self.trade_quantity) 
                   + ' ' + self.trade_direction + ' ' + str(self.trade_price))
     
    def __lt__(self, other_trade): 
        return self.trade_time < other_trade.trade_time
    
                
class Market:
    """A class object representing a stock market, which stores instances of stock trades.

    Attributes:
        trades: (lst[Trade]): A list of all trade instances in this market.
        stocks: (set(Stock)): The set of stocks which have been traded in this market.
        
    """

    def __init__(self):
        self.trades = []
        self.stocks = set()
          
    def market_trade(self, stock, trade_time, trade_quantity, trade_direction, trade_price):
        """A method which performs trades in the market and stores them in a time ordered list.

        Args:
            stock: (Stock obj): The stock being traded.
            trade_time: (datetime obj): The time at which the trade takes place.
            trade_quantity: (int): The number of stocks being traded
            trade_direction: (str): The direction of trade; either 'buy' or 'sell'.
            trade_price: (float): the price at which the stock is being traded.

        """
        trade = Trade(stock, trade_time, trade_quantity, trade_direction, trade_price)
        
        if trade_quantity > 0:
            self.trades.append(trade)
            self.trades = sorted(self.trades)
            self.stocks.add(trade.stock)
            return trade
        
    def latest_trades(self):
        """A method which gets the list of trade instances which occurred in the last 15 minutes.

        Returns:
            return: (lst[Trade]): Trade instances which occurred in the last 15 minutes.

        """
        latest_trades = [trade for trade in self.trades if (datetime.utcnow()-trade.trade_time).seconds <= 900]
        return sorted(latest_trades)
        
    def vol_weighted_stock_price(self, stock):
        """A method which calculates the volume weighted price of a given stock.

        Args:
            stock: (Stock obj)

        Returns:
            return: (float): 0 if no stocks of the specified type were exchanged.

        """
        
        trades_of_interest = [trade for trade in self.trades if trade.stock == stock and trade in self.latest_trades()]
        
        if len(trades_of_interest) > 0:
            
            numerator = sum(map(lambda trade : trade.trade_price * trade.trade_quantity, trades_of_interest))
                
            denominator = sum(map(lambda trade : trade.trade_quantity, trades_of_interest))
            
            try:
                return numerator/denominator
            except ZeroDivisionError:
                print('No stocks of the specified type were exchanged.')
                return 0
        
        else:
            print('No trades of interest')
            return 0

    def all_share_index(self):
        """A method which calculates the geometric mean of prices for all stocks traded in the market.

        Returns:
            return: (float): The geometric mean, or 0 if no trades have taken place in the market.

        """

        no_of_stocks = len(self.stocks)
        if no_of_stocks > 0:
            vol_weighted_prices = [self.vol_weighted_stock_price(stock) for stock in self.stocks]
            vol_weighted_product = functools.reduce(operator.mul, vol_weighted_prices)  
            return vol_weighted_product**(1/no_of_stocks)  
        else:
            print('No trades in market') 
            return 0
