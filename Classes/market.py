# import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import string


class StockMarket(object):
    def __init__(self, driver):
        super(StockMarket, self).__init__()
        self.driver = driver
        self.symbols = self.default_stock_symbols()

    # Method used to get stock symbols a stock exchange
    def stock_symbols_for_exchange(self, exchange):
        stock_symols = []
        # Goes alphabetically through each page to scrape each stock symbol
        for c in string.ascii_uppercase:
            list_page = 'http://www.eoddata.com/stocklist/'+exchange+'/'+c+'.htm'
            self.driver.get(list_page)
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            parent_box = soup.find('table', attrs={'class': 'quotes'})
            for child in parent_box.findAll('a'):
                if len(child.text) > 0:
                    stock_symols.append(child.text)
        return stock_symols

    def stock_symbols_for_exchanges(self, list_of_exchanges):
        stock_symbols = []
        for exchange in list_of_exchanges:
            stock_symbols.extend(self.stock_symbols_for_exchange(exchange))
        return stock_symbols

    def default_stock_symbols(self):
        symbols = []
        try:
            with open('stock_symbols.txt', 'r') as filehandle:
                for line in filehandle:
                    # remove linebreak which is the last character of the string
                    symbol = line[:-1]
                    # add item to the list
                    symbols.append(symbol)
        except FileNotFoundError:
            # If not able to read from disk, try to get from internt again
            if len(symbols) == 0:
                symbols = self.stock_symbols_for_exchanges(['NYSE', 'NASDAQ'])
                with open('stock_symbols.txt', 'a+') as filehandle:
                    for symbol in symbols:
                        filehandle.write("%s\n" % symbol)
        return symbols
