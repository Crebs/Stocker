from Classes.stock import Stock
import unittest
from selenium import webdriver


class TestStockClass(unittest.TestCase):
    """Integration Tests for Stock Class."""

    def setUp(self):
        self.driver = webdriver.Safari()

    def test_current_price(self):
        # Setup
        stock = Stock('AAPL', self.driver)
        # Test
        current_price = stock.current_stock_price()
        # Validate
        self.assertIsNotNone(current_price, 'current price should NOT return None')

if __name__ == "__main__":
    unittest.main()
