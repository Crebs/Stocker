# import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class Stock(object):
    """Call representing a  Stock."""

    def __init__(self, symbol, web_driver):
        super(Stock, self).__init__()
        self.soup = None
        self.symbol = symbol
        self.web_driver = web_driver
        self.df = None
        self.__get_quote()

    def scrape(self):
        # Collect Dates
        profit_header = self.soup.find('th', attrs={'id': 'pr-profit'})
        dates = []
        for sibling in profit_header.next_siblings:
            dates.append(sibling.text)
        roic_values = self.__roic_values()
        # initialise data of lists.
        data = {'ROIC':roic_values}
        self.df = pd.DataFrame(data, index=dates)
        print (self.df.to_string())
        return self.df

    def save(self):
        file_name = self.symbol + '.csv'
        self.df.to_csv('Data/' + file_name, index=True)

    def current_stock_price(self):
        current_price = ''
        quote_page = 'http://performance.morningstar.com/stock/performance-return.action?t='+self.symbol+'&region=usa&culture=en-US'
        try:
            self.web_driver.get(quote_page)
            soup = BeautifulSoup(self.web_driver.page_source, 'lxml')
            current_price = soup.find('span', attrs={'id': 'last-price-value'})
        except Exception as e:
            print ('Exception get current price for stock symbol: ' + self.symbol)
        return current_price

    # Private method to get stock quote from web scraping
    def __get_quote(self):
        quote_page = 'http://financials.morningstar.com/ratios/r.html?t='+self.symbol+'&region=usa&culture=en-US'
        try:
            self.web_driver.get(quote_page)
        except:
            print ('General Exception for stock symbol: ' + self.symbol)

        #begin scraping the webpage
        content = self.web_driver.page_source
        self.soup = BeautifulSoup(content, 'lxml')

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


    def free_cash_flow_per_share(self):
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

    def instrinsic_value(self, cf_past, cf_recent):
        # Calcualte Intrinsic Value of the stock
        cf_range = df.iloc[[-7,-2],[0]]
        cf_past = cf_range.iat[0,0]
        cf_recent = cf_range.iat[-1,0]
        annual_growth_rate = ((cf_recent/cf_past)**(1/5))-1
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
        return intrinsic_value
