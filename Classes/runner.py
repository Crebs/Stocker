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
                stock = Stock(symbol, self.web_driver)
                current_value = float(stock.current_stock_price())
                intrinsic_value = float(stock.intrinsic_value())
                discounted = bool(intrinsic_value > current_value)
                # Output discounted stocks only
                if discounted:
                    print ("########################")
                    print ("Scraping symbol: " + symbol)
                    print ("current value: " + str(current_value))
                    print ("intrinsic value: " + str(intrinsic_value))
                    if stock.df is not None:
                        print ("dataframe: " + stock.df.to_string())
                    print ("Discounted: " + str(discounted))
                    print ("\n\n")
                

if __name__ == "__main__":
    inputfile = None
    outputfile = ''
    driver = None
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "d:hi:o:", ["driver=", "ifile=","ofile="])
    except getopt.GetoptError:
        print ('Error: Classes.runner -d <webdriver> -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Classes.runner -d <webdriver> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-d", "--driver"):
            if arg == "safari":
                driver = webdriver.Safari()
            elif arg == "firefox":
                driver = webdriver.Firefox()

        elif opt in ("-i", "--file"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    runner = Runner(driver, inputfile)
    runner.start()
    driver.quit()
