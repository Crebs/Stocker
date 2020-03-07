# import library
from Classes.market import StockMarket
from Classes.stock import Stock
from selenium import webdriver

class Runner(object):
    """docstring for Runner."""

    def __init__(self, driver):
        super(Runner, self).__init__()
        self.market = StockMarket(driver)
        self.web_driver = driver

    def start(self):
        for symbol in self.market.symbols:
            stock = Stock(symbol, self.web_driver)
            stock.scrape()
            stock.save()

if __name__ == "__main__":
    driver = webdriver.Safari()
    runner = Runner(driver)
    runner.start()
    driver.quit()
