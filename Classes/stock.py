#!/usr/bin/python
import yfinance as yf
import pandas as pd
import os
from Classes.mstar_scraper import Scraper


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
        self.yahoo = yf.Ticker(self.symbol)
        self.market_price = self.__market_price()
        self.intrinsic_value = float(self.__intrinsic_value())

    def __intrinsic_value(self):
        try:
            # Calcualte Intrinsic Value of the stock
            cf_range = self.df.iloc[[-6,-2],:]["FCFPS"]  # free cash flow per share
            cf_past = cf_range.iloc[0]
            cf_recent = cf_range.iloc[-1]
            if float(cf_past) <= 0 or float(cf_recent) <= 0:
                print("No valid range, skipping intrinsic value calculation")
                return 0
        
            annual_growth_rate = ((cf_recent/cf_past)**(1.0/5.0))-1.0
            f_values = []
            for i in range(1,6):
                f_values.append(cf_recent*(1+annual_growth_rate)**i)
            # 10% rate of return is the more normal
            discout_rate = 0.1
            d_cf = 0
            for i in range(1,6):
                d_cf += f_values[i-1]/((1+discout_rate)**i)
            # Normal Rate of GDP is about 3%
            growth_rate = 0.03
            terminal_value = (f_values[-1]*(1+growth_rate))/(discout_rate-growth_rate)
            num_of_years = 5
            intrinsic_value = (terminal_value+d_cf)/(1+discout_rate)**num_of_years
        except Exception as e:
            intrinsic_value = 0
        return intrinsic_value

    def __quote_from_disk(self):
        try:
            df = pd.read_csv('Data/' + self.symbol + '.csv', index_col=index_name)
            return df
        except Exception as e:
            print ('Exception getting quote from disk: ' + self.symbol)
            return None