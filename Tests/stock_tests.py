from Classes.stock import Stock
import unittest
from selenium import webdriver
import pandas as pd


class TestStockClass(unittest.TestCase):
    """Integration Tests for Stock Class."""

    def setUp(self):
        self.driver = webdriver.Safari()

    def tearDown(self):
        print('tear down')
        self.driver.quit()

    def test_current_price(self):
        # Setup
        stock = Stock('AAPL', self.driver)
        # Test
        current_price = stock.current_stock_price()
        # Validate
        self.assertIsNotNone(current_price, 'current price should NOT return None')

    def test_save(self):
        # Setup
        stock = Stock('AAPL', self.driver)
        stock.scrape()
        # Test
        saved = stock.save()
        # Validate
        df = pd.read_csv('Data/' + 'AAPL.csv')
        self.assertIsNotNone(df, 'Dataframe should not be None')

if __name__ == "__main__":
    unittest.main()
