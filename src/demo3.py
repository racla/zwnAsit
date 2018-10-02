import pandas as pd
import numpy as np

'''
Problem 3
'''


import glob
import os
# 题目似乎有问题？
path =r'data\Stock4demo3' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.DataFrame()
stock_names = []
returns = []
dfs = []
for f in all_files:
    StockName = f.split("\\")[-1].split('.')[0]
    stock_names.append(StockName)
    tDF = pd.read_csv(f, index_col=0)
    returns.append(tDF["Adj Close"].diff() / tDF["Adj Close"])
    dfs.append(tDF)
    # calc return


df = pd.concat(dfs, axis=0, keys=stock_names)
return_df = pd.concat(returns, axis=1, keys=stock_names)
return_df.drop(return_df.index[0], axis=0, inplace=True)
normallized_df = (return_df-return_df.mean())/return_df.std()
# df.apply()
stock_corr = normallized_df.corr()


#是否需要给4种股票取均值
from scipy.stats import ttest_ind
statistic, p = ttest_ind(return_df["AIG"], return_df["SPY"])
statistic, p = ttest_ind(return_df["AMZN"], return_df["SPY"])
statistic, p = ttest_ind(return_df["JPM"], return_df["SPY"])
statistic, p = ttest_ind(return_df["F"], return_df["SPY"])

import matplotlib.pyplot as plt
plt.plot(return_df.index, return_df["AIG"], label="AIG")
plt.plot(return_df.index, return_df["AMZN"], label="AMZN")
plt.plot(return_df.index, return_df["JPM"], label="JPM")
plt.plot(return_df.index, return_df["F"], label="F")
plt.legend()
plt.show()
pass

'''
Problem 4
'''

raw_GDP = pd.read_excel(r'data\GDPdata4demo4\GDP.xls', skiprows=10, header=0, index_col=0)
raw_10Y = pd.read_excel(r'data\GDPdata4demo4\10Y.xls', skiprows=10, header=0, index_col=0)
raw_2Y = pd.read_excel(r'data\GDPdata4demo4\2Y.xls', skiprows=10, header=0, index_col=0)
reindexed_GDP = raw_GDP.reindex(raw_10Y.index)
reindexed_GDP.iloc[0] = -1.73
reindexed_GDP = reindexed_GDP.interpolate(method='linear')


delta_10Y_2Y = raw_10Y["GS10"]-raw_2Y["GS2"]
delta_10Y_2Y.columns = ['Diff']
import matplotlib.pyplot as plt
from scipy import signal
plt.subplot(3,1,1)
plt.plot(reindexed_GDP.index.values, reindexed_GDP.values, label="reindexed")
plt.plot(raw_GDP.index.values, raw_GDP.values, label="raw")
plt.title('GDP')
plt.legend()
plt.subplot(3,1,2)
plt.plot(raw_10Y.index.values, delta_10Y_2Y.values)
plt.title('10Y-2Y')

#corr0 = signal.correlate(reindexed_GDP['A191RP1Q027SBEA'].values, delta_10Y_2Y.values)
corr1 = np.correlate(reindexed_GDP['A191RP1Q027SBEA'].values, delta_10Y_2Y.values, "full")
np.where(corr1==np.sort(corr1)[-1])
#plt.plot(raw_2Y.index.values, raw_2Y.values)
plt.subplot(3,1,3)
plt.plot(corr1)
plt.title('corr')

plt.show()
pass
