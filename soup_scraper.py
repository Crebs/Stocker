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

# Get Date columns
profit_header = soup.find('th', attrs={'id': 'pr-profit'})
# print (profit_header.text)
# Collect Dates
dates = []
for sibling in profit_header.next_siblings:
    dates.append(sibling.text)

# Return on Invested Capital
roic_box = soup.find('th', attrs={'id': 'i27'})
# print (roic_box.text)
# Collect Values
values = []
for child in roic_box.parent.findAll('td'):
    values.append(child.text)

# initialise data of lists.
data = {profit_header.text:values}

# Creates pandas DataFrame.
df = pd.DataFrame(data, index =dates)

# print the data
print (df)

# Clean up
driver.quit()
