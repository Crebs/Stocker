from Classes.stock import Stock
import unittest
from selenium import webdriver
import pandas as pd


class TestStockClass(unittest.TestCase):
    """Integration Tests for Stock Class."""

    def setUp(self):
        self.driver = webdriver.Safari()
        self.test_symbol = 'AAPL'
        self.sut = Stock(self.test_symbol, self.driver)

    def tearDown(self):
        self.driver.quit()
        self.sut.delete()

    def test_current_price(self):
        # Setup and Test
        current_price = self.sut.current_stock_price()
        # Validate
        self.assertIsNotNone(current_price, 'current price should NOT return None')

    def test_save(self):
        # Setup
        self.sut.scrape()
        # Test
        saved = self.sut.save()
        # Validate
        df = pd.read_csv('Data/' + 'AAPL.csv')
        self.assertIsNotNone(df, 'Dataframe should not be None')

if __name__ == "__main__":
    unittest.main()
