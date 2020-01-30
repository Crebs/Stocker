# import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Safari()

# specify the url
quote_page = 'http://financials.morningstar.com/ratios/r.html?t=ADBE&region=usa&culture=en-US'

driver.get(quote_page)
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')

roic_box = soup.find('th', attrs={'id': 'i27'})

print (roic_box.text)
for child in roic_box.parent.findAll('td'):
    print (child.text)
driver.quit()
