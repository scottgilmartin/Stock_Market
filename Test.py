from Stock_Market import Stock, Trade, Market
from datetime import datetime, timedelta
import unittest


class StockTests(unittest.TestCase):
    
    # create stocks and test the methods
    
    def setUp(self):
        self.tea_stock = Stock('TEA', 'common', 0, 100)
        self.pop_stock = Stock('POP', 'common', 8, 100)
        self.gin_stock = Stock('GIN', 'preferred', 8, 100, 0.02)
        
    def test_dividend_yield(self):
        self.assertEqual(self.tea_stock.dividend_yield(5), 0)
        self.assertEqual(self.tea_stock.dividend_yield(0), 0)
        
        self.assertEqual(self.pop_stock.dividend_yield(5), self.pop_stock.last_dividend/5)
        self.assertEqual(self.pop_stock.dividend_yield(0), 0)
        
        self.assertEqual(self.gin_stock.dividend_yield(5),
                         (self.gin_stock.fixed_dividend * self.gin_stock.par_value) / 5)
        self.assertEqual(self.gin_stock.dividend_yield(0), 0)
        
    def test_p_e_ratio(self):
        self.assertEqual(self.tea_stock.p_e_ratio(0), 0)
        self.assertEqual(self.tea_stock.p_e_ratio(5), 0)
        
        self.assertEqual(self.pop_stock.p_e_ratio(0), 0)
        self.assertEqual(self.pop_stock.p_e_ratio(5), 5/self.pop_stock.dividend_yield(5))
        
        self.assertEqual(self.gin_stock.p_e_ratio(0), 0)
        self.assertEqual(self.gin_stock.p_e_ratio(5), 5/self.gin_stock.dividend_yield(5))
        

class MarketTests(unittest.TestCase):
    
    # create stocks and a market
    
    def setUp(self):
        self.tea_stock = Stock('TEA', 'common', 0, 100)
        self.pop_stock = Stock('POP', 'common', 8, 100)
        self.gin_stock = Stock('GIN', 'preferred', 8, 100, 0.02)
        self.joe_stock = Stock('JOE', 'common', 13, 250)
        self.ale_stock = Stock('ALE', 'common', 23, 60)
        self.market = Market()
        
        # perform trades in the market
        
        self.trade_tea_buy = self.market.market_trade(self.tea_stock, datetime.utcnow(), 400, 'buy', 5)
        self.trade_tea_sell = self.market.market_trade(self.tea_stock, datetime.utcnow(), 100, 'sell', 4)
        
        self.trade_pop_buy = self.market.market_trade(self.pop_stock, datetime.utcnow(), 400, 'buy', 5)
        self.trade_pop_sell = self.market.market_trade(self.pop_stock, datetime.utcnow(), 100, 'sell', 4)
        
        self.trade_gin_buy = self.market.market_trade(self.gin_stock, datetime.utcnow(), 100, 'buy', 8)
        self.trade_ale_buy = self.market.market_trade(self.ale_stock, datetime.utcnow(), 0, 'buy', 8)
        
        self.trade_pop_14_min_ago = self.market.market_trade(self.pop_stock,
                                                             datetime.utcnow()-timedelta(minutes=14), 300, 'buy', 7)
        self.trade_pop_16_min_ago = self.market.market_trade(self.pop_stock,
                                                             datetime.utcnow()-timedelta(minutes=16), 300, 'buy', 5)
        
        self.trade_pop_buy_zero = self.market.market_trade(self.pop_stock, datetime.utcnow(), 0, 'buy', 9)
        self.trade_pop_buy_free = self.market.market_trade(self.pop_stock, datetime.utcnow(), 100, 'buy', 0)
        self.trade_pop_buy_zero_free = Trade(self.pop_stock, datetime.utcnow(), 0, 'buy', 0)
        
        # test the market methods
                 
    def test_latest_trades(self):
        self.assertTrue(self.trade_pop_buy in self.market.latest_trades())
        self.assertTrue(self.trade_pop_14_min_ago in self.market.latest_trades())
        # trade made 14 minutes ago should be considered a latest trade
        self.assertFalse(self.trade_pop_16_min_ago in self.market.latest_trades())
        # trade made 16 minutes ago should not be considered a latest trade
                
    def test_vol_weighted_stock_price(self):
        self.assertEqual(self.market.vol_weighted_stock_price(self.tea_stock), 24/5)
        self.assertEqual(self.market.vol_weighted_stock_price(self.pop_stock), (24+21)/(5+3+1))
        self.assertEqual(self.market.vol_weighted_stock_price(self.gin_stock), 8)
        
        self.assertEqual(self.market.vol_weighted_stock_price(self.joe_stock), 0)
        # make sure we ignore stocks which haven't been traded
        self.assertEqual(self.market.vol_weighted_stock_price(self.ale_stock), 0)
        # make sure we ignore trades of zero quantity
    
    def test_all_share_index(self):
        self.assertEqual(self.market.all_share_index(), (4.8*5*8)**(1/3))
        
              
if __name__ == '__main__':
    unittest.main()

