#!/usr/bin/python
from Classes.indicator import Indicator
import yfinance as yf
import pandas as pd
import os
from Classes.web_scraper import Scraper


index_name = 'Date'
class Stock(object):
    """Call representing a  Stock."""

    def __init__(self, symbol, scraper):
        super(Stock, self).__init__()
        self.symbol = symbol
        self.scraper = scraper
        self.df = None 
        self.intrinsic_value = None
        self.yahoo = yf.Ticker(self.symbol)
        self.market_price = None

    def save(self):
        file_name = self.symbol + '.csv'
        if self.df is not None:
            self.df.to_csv('Data/' + file_name, index=True)

    def delete(self):
        file_name = self.symbol + '.csv'
        try:
            os.remove('Data/'+ file_name)
        except Exception:
            print('Not able to delete '+ file_name + ', file not found')

    def is_a_buy(self):
        #TODO: need to come up with buying rules.  Also, can we add Machine learning or AI here?
        iv = self.intrinsic_value
        try:
            cv = self.market_price
        except Exception:
            cv = 0
        return float(iv) > float(cv)

    def __market_price(self):
        price = self.yahoo.info["regularMarketPrice"]
        if price == None:
            price = self.scraper.get_current_stock_price(self.symbol)
        return price
    
    def scrape(self):
        self.df = self.__quote_from_disk()
        if self.df is None:
            self.df = self.scraper.scrape(self.symbol)
            self.save()
        indicator = Indicator(self.df)
        self.yahoo = yf.Ticker(self.symbol)
        self.market_price = self.__market_price()
        self.intrinsic_value = float(indicator.intrinsic_value())

    def __quote_from_disk(self):
        try:
            df = pd.read_csv('Data/' + self.symbol + '.csv', index_col=index_name)
            return df
        except Exception as e:
            print ('Exception getting quote from disk: ' + self.symbol)
            return None