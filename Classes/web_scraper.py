from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class Scraper(object):
    def __init__(self, driver_type):
        super(Scraper, self).__init__()
        if driver_type == "safari":
            self.web_driver = webdriver.Safari()
        elif driver_type == "firefox":
            self.web_driver = webdriver.Firefox()

    def scrape(self, symbol):
        ratios_page = 'http://financials.morningstar.com/ratios/r.html?t='+symbol+'&region=usa&culture=en-US'
        html = self.__get_html(ratios_page, "th")
        soup = BeautifulSoup(html, features="html.parser")
        df = self.__get_data_frame(soup)
        return df

    def get_current_stock_price(self, symbol):
        current_price = 0
        try:
            page = 'http://performance.morningstar.com/stock/performance-return.action?t='+symbol+'&region=usa&culture=en-US'
            html = self.__get_html(page, "span")
            soup = BeautifulSoup(html, features="html.parser")
            current_price = float(soup.find('span', attrs={'id': 'last-price-value'}).text)
        except Exception as e:
            print ('Exception get current price for stock symbol: ' + symbol)
            return current_price
        return current_price
    
    def quit(self):
        self.web_driver.quit()

    def __get_html(self, url, tag):
        self.web_driver.get(url)
        el = WebDriverWait(self.web_driver, timeout=3).until(lambda d: d.find_element_by_tag_name(tag))
        return self.web_driver.page_source
            
    def __get_roic_values(self, soup):
        # Return on Invested Capital
        roic_box = soup.find('th', attrs={'id': 'i27'})
        # Collect Values
        values = []
        for child in roic_box.parent.findAll('td'):
            value = child.text
            if isfloat(value):
                values.append(float(value))
            else:
                values.append(0)
        return values
    
    def __get_free_cash_flow_per_share(self, soup):
        cf_values = []
        free_cash_flow_per_share_header = soup.find('th', attrs={'id': 'i90'})
        if free_cash_flow_per_share_header is not None:
            for child in free_cash_flow_per_share_header.parent.findAll('td'):
                value = child.text
                if isfloat(value):
                    cf_values.append(float(child.text))
                else:
                    cf_values.append(0)
        return cf_values

    def __get_data_frame(self, soup):
        profit_header = soup.find('th', attrs={'id': 'pr-profit'})
        dates = []
        if profit_header is not None:
            for sibling in profit_header.next_siblings:
                dates.append(sibling.text)
            roic_values = self.__get_roic_values(soup)
            fcfps_values = self.__get_free_cash_flow_per_share(soup)
            # initialise data of lists.
            data = {'ROIC':roic_values, 'FCFPS':fcfps_values,}
            if len(data) > 0:
                try:
                    df = pd.DataFrame(data, index=dates)
                    df.index.name = 'Date'
                    return df
                except Exception as e:
                    print('issue creating data frame')
                    return None
        return None