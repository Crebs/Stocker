#!/usr/bin/python
import pandas as pd

class Indicator(object):
    def __init__(self, df):
        super(Indicator, self).__init__()
        self.df = df

    def intrinsic_value(self):
        try:
            # Calcualte Intrinsic Value of the stock
            number_years = 5 # this is up to preference, but most recomend 5 years
            cf_range = self.df.iloc[-6:-1]["FCFPS"]  # free cash flow per share
            cf_past_index = 0
            cf_past = cf_range.iloc[cf_past_index]
            cf_recent = cf_range.iloc[-1]

            while(cf_past <= 0 and number_years > 1):
                print("Update Range")
                cf_past_index += 1
                number_years -= 1
                cf_past = cf_range.iloc[cf_past_index]
                print("New past value: " + str(cf_past))
                print("Range of years: " + str(number_years))

            if float(cf_past) <= 0 or float(cf_recent) <= 0:
                print("No valid range, skipping intrinsic value calculation")
                return 0
        
            annual_growth_rate = ((cf_recent/cf_past)**(1.0/number_years))-1.0
            f_values = []
            for i in range(1,number_years+1):
                f_values.append(cf_recent*(1+annual_growth_rate)**i)
            # 10% rate of return is the more normal
            discout_rate = 0.1
            d_cf = 0
            for i in range(1,number_years+1):
                d_cf += f_values[i-1]/((1+discout_rate)**i)
            # Normal Rate of GDP is about 3%
            growth_rate = 0.03
            terminal_value = (f_values[-1]*(1+growth_rate))/(discout_rate-growth_rate)
            intrinsic_value = (terminal_value+d_cf)/(1+discout_rate)**number_years
        except Exception as e:
            intrinsic_value = 0
        return intrinsic_value