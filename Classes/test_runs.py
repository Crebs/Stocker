
import pandas as pd

class TestRun(object):

    def intrinsic_value(self):
        df = pd.read_csv('Data/SONO.csv', index_col="Date")
        print(df)
        print("##################")
        cf_range = df.iloc[[-6,-2],:]["FCFPS"]  # free cash flow per share
        print(cf_range)
        print("##################")
        item = df.iloc[-6:-1]["FCFPS"]
        print(item)
        print("##################")
        cf_past = cf_range.iloc[0]
        cf_recent = cf_range.iloc[-1]
        print(str(cf_past))
        print(str(cf_recent))
        print("##################")
        p_i = 0
        cf_past = item.iloc[0]
        cf_recent = item.iloc[-1]
        print(str(cf_past))
        print(str(cf_recent))
        print("##################")
        years = 5
        while(cf_past <= 0):
            p_i += 1
            years -= 1
            cf_past = item.iloc[p_i]
            print("new past value: " + str(cf_past))
            print("range of years: " + str(years))

        print("##################")
        annual_growth_rate = ((cf_recent/cf_past)**(1.0/years))-1.0
        print("annual_grow_rate: " + str(annual_growth_rate))
        print("##################")
        f_values = []
        for i in range(1,years+1):
            f_values.append(cf_recent*(1+annual_growth_rate)**i)
        print(f_values)
        print("##################")
        discout_rate = 0.1
        d_cf = 0
        for i in range(1,years+1):
            d_cf += f_values[i-1]/((1+discout_rate)**i)
        print(str(d_cf))
        print("##################")
        growth_rate = 0.03
        terminal_value = (f_values[-1]*(1+growth_rate))/(discout_rate-growth_rate)
        intrinsic_value = (terminal_value+d_cf)/(1+discout_rate)**years
        print("intrinsic value: " + str(intrinsic_value))

if __name__ == "__main__":
    tr = TestRun()
    tr.intrinsic_value()