#!/usr/bin/python
from Classes.market import StockMarket
from Classes.stock import Stock
from Classes.web_scraper import Scraper
import sys, getopt

class Runner(object):
    """docstring for Runner."""

    def __init__(self, driver_name, symbols_file=None):
        super(Runner, self).__init__()
        self.scraper = Scraper(driver_name)
        self.market = StockMarket(symbols_file)

    def start(self):
        for symbol in self.market.symbols:
            if len(symbol) > 0:
                stock = Stock(symbol, self.scraper)
                stock.scrape()
                intrinsic_value = stock.intrinsic_value
                market_price = stock.market_price
                # Output discounted stocks only
                # if discounted:
                print ("########################")
                print ("Scraping symbol: " + symbol)
                print ("current value: " + str(market_price))
                print ("intrinsic value: " + str(intrinsic_value))
                if stock.df is not None:
                    print ("dataframe: " + stock.df.to_string())
                print ("Discounted: " + str(stock.is_a_buy()))
                if market_price > 0:
                    ratio = intrinsic_value/market_price
                    succes_color = "\033[92m"
                    fail_color = "\033[91m"
                    text_color = fail_color
                    if ratio > 0.7:
                        text_color = succes_color
                    print ("intrinsic / current ratio: " + text_color + str(ratio) + "\033[0m")
                print ("\n\n")
    
    def quit(self):
        self.scraper.quit()
                
if __name__ == "__main__":
    inputfile = None
    outputfile = ''
    driver_name = ''
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
            driver_name = arg
        elif opt in ("-i", "--file"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    runner = Runner(driver_name, inputfile)
    runner.start()
    runner.quit()
