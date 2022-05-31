from Classes.stock import Stock
import unittest
from selenium import webdriver
import pandas as pd


class TestStockClass(unittest.TestCase):
    """Integration Tests for Stock Class."""

    def setUp(self):
        self.driver = webdriver.Safari()
        self.test_symbol = 'TGT'
        self.sut = Stock(self.test_symbol, self.driver)

    def tearDown(self):
        self.driver.quit()
        # self.sut.delete()

    def test_current_price(self):
        # Setup and Test
        current_price = self.sut.current_stock_price()
        # Validate
        self.assertIsNotNone(current_price, 'current price should NOT return None')

    def test_save(self):
        # Setup
        # Test
        self.sut.save()
        # Validate
        df = pd.read_json('Data/' + 'AAPL.json')
        self.assertIsNotNone(df, 'Dataframe should not be None')

    def test_intrinsic_value(self):
        # Setup
        # Test
        intrinsic_value = self.sut.intrinsic_value()

        # Validate
        self.assertGreater(intrinsic_value, 0, "intrinsit value should be greater than zero")

if __name__ == "__main__":
    unittest.main()
