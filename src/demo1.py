import numpy as np
import pandas as pd
from scipy import linalg
from numpy import dot
def test_funtion1():
    A = np.mat([[1, 2, 1], [2, 3, 1], [3, 4, 1], [4, 5, 1]])
    # u, s, v = np.linalg.svd(A)
    print(np.linalg.matrix_rank(A))
    b = np.mat([3, 1, 2, 5])
    B = linalg.orth(A)
    p = dot(dot(dot(B , np.mat(dot(B.T , B)).I) , B.T) , b.T)
    print(p)


def test_function2():
    from matplotlib import  pyplot as plt
    window_size = 50

    data = generate_data()


    start = pd.Timestamp('2018-09-24 00:00:00')
    end = pd.Timestamp('2018-09-24 16:30:00')
    t = np.linspace(start.value, end.value, 100)
    t = pd.to_datetime(t)

    aligned_data = data.reindex(t)
    ipt_data =  aligned_data.interpolate(method='nearest')

    index = 0
    array_size = ipt_data.loc[:].__len__()
    statis_list = []
    while True:
        if index + window_size > array_size:
            break

        statis_list.append(ipt_data.iloc[index: index+window_size-1].describe())
        index = index + 1


    plt.subplot(2, 1, 1)
    plt.plot(aligned_data.index, aligned_data.loc[:])
    plt.subplot(2, 1, 2)
    plt.plot(ipt_data.index, ipt_data.loc[:])
    plt.show()

    pass


def generate_data():
    df = pd.read_csv('data/data.csv', encoding='utf-8', index_col=0)
    df.index = pd.to_datetime(df.index)
    return df

#test_funtion1()
test_function2()