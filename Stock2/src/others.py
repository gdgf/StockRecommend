import os
import pandas as pd
import numpy as np
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块

import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential  # Sequential是多个网络层的线性堆叠
from keras.layers import Dense  # 全连接层
from keras.layers import LSTM  #
from keras.layers import Dropout  # 正则化方法：Dropout


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示



# 训练模型
def trainmodel(name):
    if not os.path.exists("../model/" + name + ".h5"):  # 如果模型不存在
        print('开始训练模型\n')
        dataset = pd.read_csv('./data/Train/' + name + '_Train.csv', index_col="Date", parse_dates=True)
        # 以开盘价为训练数据
        training_set = dataset['Open']
        training_set = pd.DataFrame(training_set)
        print(training_set)
        sc = MinMaxScaler(feature_range=(0, 1))
        training_set_scaled = sc.fit_transform(training_set)

        X_train = []
        y_train = []
        print("数据集大小:",len(dataset))
        for i in range(60, len(dataset)):
            X_train.append(training_set_scaled[i - 60:i, 0])  # 其实共1列，所以，0列的i-60 到i的数据
            y_train.append(training_set_scaled[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        print(X_train)

        regressor = Sequential()
        regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.2))

        regressor.add(Dense(units=1))

        regressor.compile(optimizer='adam', loss='mean_squared_error')
        regressor.fit(X_train, y_train, epochs=100,batch_size=32)
        regressor.save("../model/"+name+".h5", overwrite=True, include_optimizer=True)
        tkinter.messagebox.showinfo(title='提醒', message='模型训练完成，将继续！')  # 提示信息对话窗
    else:
        tkinter.messagebox.showinfo(title='提醒', message='模型已存在，将继续！')  # 提示信息对话窗

# 涨
def getrise(data):
    count = 0
    for x in data['p_change'] >= 0:
        if x:
            count = count + 1
    return count / len(data)


# 跌
def getdrop(data):
    count = 0
    for x in data['p_change'] < 0:
        if x:
            count = count + 1
    return count / len(data)
