#!/usr/bin/python

# import library
from Classes.market import StockMarket
from Classes.stock import Stock
from selenium import webdriver

import sys, getopt

class Runner(object):
    """docstring for Runner."""

    def __init__(self, driver, symbols_file=None):
        super(Runner, self).__init__()
        self.market = StockMarket(driver, symbols_file)
        self.web_driver = driver

    def start(self):
        for symbol in self.market.symbols:
            if len(symbol) > 0:
                print "Scraping symbol: " + symbol
                stock = Stock(symbol, self.web_driver)
                intrinsic_value = stock.intrinsic_value()
                current_value = stock.current_stock_price()
                print "intrinsic value: " + str(intrinsic_value)
                print "current value: " + str(current_value)
                if stock.df is not None:
                    print "dataframe: " + stock.df.to_string()
                print "is a good buy: " + str(stock.is_a_buy())
                

if __name__ == "__main__":
    inputfile = None
    outputfile = ''
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print 'Classes.runner -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Classes.runner -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--file"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    driver = webdriver.Safari()
    runner = Runner(driver, inputfile)
    runner.start()
    driver.quit()
