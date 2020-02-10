# import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import string

driver = webdriver.Safari()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#http://www.eoddata.com/stocklist/NYSE/B.htm

# http://performance.morningstar.com/stock/performance-return.action?t=CRM&region=usa&culture=en-US
stock_symols = []

exchanges = ['NYSE', 'NASDAQ']
for exchange in exchanges:
    for c in string.ascii_uppercase:
        list_page = 'http://www.eoddata.com/stocklist/'+exchange+'/'+c+'.htm'
        driver.get(list_page)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        parent_box = soup.find('table', attrs={'class': 'quotes'})
        for child in parent_box.findAll('a'):
            if len(child.text) > 0:
                stock_symols.append(child.text)

for t in stock_symols:
    # specify the url
    quote_page = 'http://financials.morningstar.com/ratios/r.html?t='+t+'&region=usa&culture=en-US'

    try:
      driver.get(quote_page)
    except ValueError:
      print ('Failed to load page for stock symbol: ' + t)
      continue

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # Get Date columns
    profit_header = soup.find('th', attrs={'id': 'pr-profit'})


    intrinsic_value = 0
    if profit_header is not None:
        # Collect Dates
        dates = []
        for sibling in profit_header.next_siblings:
            dates.append(sibling.text)

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

        # Free Cash Flow Per Share
        free_cash_flow_per_share_header = soup.find('th', attrs={'id': 'i90'})
        if free_cash_flow_per_share_header is not None:
            cf_values = []
            for child in free_cash_flow_per_share_header.parent.findAll('td'):
                value = child.text
                if isfloat(value):
                    cf_values.append(float(child.text))
                else:
                    cf_values.append(0)

            # initialise data of lists.
            data = {roic_box.text:values, free_cash_flow_per_share_header.text:cf_values}

            # Creates pandas DataFrame.
            df = pd.DataFrame(data, index =dates)

            # Generally we're only interested in stock with good Return on Invested Captical
            avg_roic = df.loc[:,roic_box.text].mean()

            if avg_roic >= 20:
                # Calcualte Intrinsic Value of the stock
                cf_range = df.iloc[[-7,-2],[0]]
                cf_past = cf_range.iat[0,0]
                cf_recent = cf_range.iat[-1,0]
                annual_growth_rate = ((cf_recent/cf_past)**(1/5))-1
                f_values = []
                for i in range(1,6):
                    f_values.append(cf_recent*(1+annual_growth_rate)**i)
                # 10% rate of return is the more normal
                discout_rate = 0.1
                d_cf = 0
                for i in range(1,6):
                    d_cf += f_values[i-1]/((1+discout_rate)**i)
                # Normal Rate of GDP is about 3%
                growth_rate = 0.03
                terminal_value = (f_values[-1]*(1+growth_rate))/(discout_rate-growth_rate)
                num_of_years = 5
                intrinsic_value = (terminal_value+d_cf)/(1+discout_rate)**num_of_years

                # Get listed valuex
                quote_page = 'http://performance.morningstar.com/stock/performance-return.action?t='+t+'&region=usa&culture=en-US'
                driver.get(quote_page)
                content = driver.page_source
                soup = BeautifulSoup(content, 'lxml')
                last_price_span = soup.find('span', attrs={'id': 'last-price-value'})

                if last_price_span is not None:
                    if float(last_price_span.text) < intrinsic_value:
                        print('UNDERVALUED STOCK')
                        print('symbol: ' + t)
                        print (df)
                        print('Last Price: ' + last_price_span.text)
                        print('Intrinsic Value: ' + str(intrinsic_value))
                        print('Average Return on Invested Capital: '+ str(avg_roic))
        else:
            print ("Issue evaluating " + t)

# Clean up
driver.quit()
