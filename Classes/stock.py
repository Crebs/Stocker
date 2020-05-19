# import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

index_name = 'Date'
class Stock(object):
    """Call representing a  Stock."""

    def __init__(self, symbol, web_driver):
        super(Stock, self).__init__()
        self.soup = None
        self.symbol = symbol
        self.web_driver = web_driver
        self.df = None
        # Need to scrape all the data for the stock before any calculations can be performed
        self.__scrape()

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
        iv = self.intrinsic_value()
        try:
            cv = float(self.current_stock_price())
        except Exception:
            cv = 0
        return iv > cv

    def intrinsic_value(self):
        try:
            # Calcualte Intrinsic Value of the stock
            cf_range = self.df.iloc[[-7,-2],[0]]
            cf_past = cf_range.iat[0,0]
            cf_recent = cf_range.iat[-1,0]
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


    def current_stock_price(self):
        current_price = ''
        quote_page = 'http://performance.morningstar.com/stock/performance-return.action?t='+self.symbol+'&region=usa&culture=en-US'
        try:
            self.web_driver.get(quote_page)
            soup = BeautifulSoup(self.web_driver.page_source, features="html.parser")
            current_price = soup.find('span', attrs={'id': 'last-price-value'}).text
        except Exception as e:
            print ('Exception get current price for stock symbol: ' + self.symbol + " with error " + e.strerror)
            with open('not_found_stock_symbols.txt', 'a+') as filehandle:
                filehandle.write("%s\n" % self.symbol)
        return current_price

    def __scrape(self):
        self.df = self.__quote_from_disk()
        if self.df is None:
            self.__get_quote()
            # Collect Dates
            if self.soup is not None:
                profit_header = self.soup.find('th', attrs={'id': 'pr-profit'})
                dates = []
                if profit_header is not None:
                    for sibling in profit_header.next_siblings:
                        dates.append(sibling.text)
                    roic_values = self.__roic_values()
                    fcfps_values = self.__free_cash_flow_per_share()
                    # initialise data of lists.
                    data = {'ROIC':roic_values, 'FCFPS':fcfps_values,}
                    if len(data) > 0:
                        try:
                            self.df = pd.DataFrame(data, index=dates)
                            self.df.index.name = index_name
                            self.save()
                        except Exception as e:
                            print('value issue with ' + self.symbol + ' error: ' + e.strerror)
                            with open('not_found_stock_symbols.txt', 'a+') as filehandle:
                                filehandle.write("%s\n" % self.symbol)
                            self.df = None
            else:
                print('soup None on ' + self.symbol)


        return self.df

    def __quote_from_disk(self):
        try:
            df = pd.read_csv('Data/' + self.symbol + '.csv', index_col=index_name)
            return df
        except Exception as e:
            print ('Exception getting quote from disk: ' + self.symbol + ' reason ' + e.strerror)
            return None

    # Private method to get stock quote from web scraping
    def __get_quote(self):
        if self.df is None:
            quote_page = 'http://financials.morningstar.com/ratios/r.html?t='+self.symbol+'&region=usa&culture=en-US'
            try:
                time.sleep(2.5)
                self.web_driver.get(quote_page)
                self.soup = BeautifulSoup(self.web_driver.page_source, features="html.parser")
            except:
                print ('General Exception for stock symbol: ' + self.symbol)
                with open('not_found_stock_symbols.txt', 'a+') as filehandle:
                    filehandle.write("%s\n" % self.symbol)
        else:
            print('Symbol read from disk. Skipping network request.')


    def __roic_values(self):
        # Return on Invested Capital
        roic_box = self.soup.find('th', attrs={'id': 'i27'})
        # Collect Values
        values = []
        for child in roic_box.parent.findAll('td'):
            value = child.text
            if isfloat(value):
                values.append(float(value))
            else:
                values.append(0)
        return values


    def __free_cash_flow_per_share(self):
        cf_values = []
        free_cash_flow_per_share_header = self.soup.find('th', attrs={'id': 'i90'})
        if free_cash_flow_per_share_header is not None:
            for child in free_cash_flow_per_share_header.parent.findAll('td'):
                value = child.text
                if isfloat(value):
                    cf_values.append(float(child.text))
                else:
                    cf_values.append(0)
        return cf_values
