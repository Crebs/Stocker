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
# Collect Dates
dates = []
for sibling in profit_header.next_siblings:
    dates.append(sibling.text)

# Return on Invested Capital
roic_box = soup.find('th', attrs={'id': 'i27'})
# Collect Values
values = []
for child in roic_box.parent.findAll('td'):
    values.append(child.text)

# Free Cash Flow Per Share
free_cash_flow_per_share_header = soup.find('th', attrs={'id': 'i90'})
print (free_cash_flow_per_share_header.text)
cf_values = []
for child in free_cash_flow_per_share_header.parent.findAll('td'):
    cf_values.append(child.text)

# initialise data of lists.
data = {roic_box.text:values, free_cash_flow_per_share_header.text:cf_values}

# Creates pandas DataFrame.
df = pd.DataFrame(data, index =dates)

# print the data
print (df)

cf_range = df.iloc[[-7,-2],[0]]

cf_past = float(cf_range.iat[0,0])
cf_recent = float(cf_range.iat[-1,0])
annual_growth_rate = ((cf_recent/cf_past)**(1/5))-1
# print (annual_growth_rate)

f_values = []
for i in range(1,6):
    f_values.append(cf_recent*(1+annual_growth_rate)**i)
# print (f_values)

discout_rate = 0.1
d_cf = 0
for i in range(1,6):
    d_cf += f_values[i-1]/((1+discout_rate)**i)
# print (d_cf)

growth_rate = 0.03
terminal_value = (f_values[-1]*(1+growth_rate))/(discout_rate-growth_rate)
# print(terminal_value)

num_of_years = 5
intrinsic_value = (terminal_value+d_cf)/(1+discout_rate)**num_of_years
print(intrinsic_value)


# Clean up
driver.quit()
