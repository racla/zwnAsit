# -*- coding:utf-8 -*-
# Abstract : multi index; DataFrame;
# Created  : Sat Sep 29 2018 12:44:56 GMT+0800
# Author   : Charles

import pandas as pd
import numpy as np

'''
Problem 1 
'''

letters = ['A', 'B', 'C']
numbers = list(range(10))

# FYI: http://pandas.pydata.org/pandas-docs/stable/advanced.html?highlight=lexsort

mi = pd.MultiIndex.from_product([letters,  numbers])
s = pd.Series(np.random.rand(30), index=mi)

#1.
s.index.is_lexsorted()
# s.sort_index(inplace=True)

#2.
print(s.loc[:, [1, 3, 6]])

#3.
idx = pd.IndexSlice
s.loc[idx[:'B', 5:]]


s.loc[(slice(None, 'B'), slice(5, 'None'))]

#4.
s_new = s.swaplevel()
s_new.index.is_lexsorted()
s_new_sorted = s_new.sort_index()


'''
Problem 2
'''
df = pd.DataFrame({'From_To': ['LoNDon_paris', 'MAdrid_miLAN', 'londON_StockhOlm',
                  'Budapest_PaRis', 'Brussels_londOn'],
                  'FlightNumber': [10045, np.nan, 10065, np.nan, 10085],
                  'RecentDelays': [[23, 47], [], [24, 43, 87], [13], [67, 32]],
                  'Airline': ['KLM(!)', '<Air France> (12)', '(British Airways. )',
                  '12. Air France', '"Swiss Air"']})

# 1.
#df['FlightNumber'].loc[1] = (df['FlightNumber'].iloc[0] + 10)
#df['FlightNumber'].loc[3] = (df['FlightNumber'].iloc[2] + 10)
df['FlightNumber'].interpolate(method='linear', inplace=True)
df['FlightNumber'] = df['FlightNumber'].astype(int)


# 2.
tmpDF = pd.DataFrame(df["From_To"])
tmpDF['From'] = tmpDF["From_To"].str.split('_').str[0]
tmpDF['To'] = tmpDF["From_To"].str.split('_').str[1]
tmpDF = tmpDF.drop('From_To', 1)



#3.
tmpDF['From'] = tmpDF["From"].str.title()
tmpDF['To'] = tmpDF["To"].str.title()

#4.
df = df.drop('From_To', 1)
df = pd.concat([tmpDF,df], axis = 1)

#5.
FixAirline = pd.DataFrame(df.Airline)

a = '()<>1234567890,.?!""[]{} '
#FixAirline['Airline'] = FixAirline['Airline'].map(lambda x: x.strip(a))
import re
FixAirline['Airline'] = FixAirline['Airline'].map(lambda x: re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', '', x))
df = df.drop('Airline', 1)
df = pd.concat([df, FixAirline], axis = 1)

#6.
tDelay = pd.DataFrame(df['RecentDelays'])
tDelay = pd.DataFrame(df['RecentDelays'].values.tolist())
tDelay.columns = ['Delay_1', 'Delay_2', 'Delay_3']
df = df.drop('RecentDelays', 1)
df.insert(3, "Delay_1", tDelay['Delay_1'])
df.insert(4, "Delay_2", tDelay['Delay_2'])
df.insert(5, "Delay_3", tDelay['Delay_3'])
print(df)