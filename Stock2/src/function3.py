
import os
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import datetime

import tkinter as tk
import tkinter.messagebox  # 要使用messagebox先要导入模块

from tkinter.scrolledtext import ScrolledText
from src.others import trainmodel
from src.getdata import getdata

import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# main
def Forecast():

    company = tk.StringVar()
    date = tk.StringVar()
    dateTest=tk.StringVar()
    # 开始预测函数
    def startyuce():
        # 得到公司名字和日期
        name= company.get()
        N=date.get()
        getdata(name) # 获取数据
        trainmodel(name) # 训练模型
        forecast(name,N)

    def startyanzhen():
        name = company.get()
        N = dateTest.get()
        yanzheng(name,N)

    top = tk.Toplevel()
    top.title('股票推荐与分析')
    top.geometry('1000x800')  # 这里的乘是小x

    tk.Label(top, text='填写公司名字:', font=('Arial', 12)).place(x=10, y=10)
    tk.Label(top, text='预测将来N天的开盘价:', font=('Arial', 12)).place(x=10, y=100)
    tk.Label(top, text='验证N天的开盘价:', font=('Arial', 12)).place(x=10, y=200)

    company.set('GOOG')
    entry_company = tk.Entry(top, textvariable=company, font=('Arial', 12)).place(x=200, y=10)

    date.set('5')
    entry_date = tk.Entry(top, textvariable=date, font=('Arial', 12)).place(x=200, y=110)

    temp = pd.read_csv("./data/Test/GOOG_Test.csv")
    n = len(temp)

    dateTest.set("N<="+str(n))
    entry_datetest = tk.Entry(top, textvariable=dateTest, font=('Arial', 12)).place(x=200, y=210)


    # 股票数据每公布一天，就将其加在里面，重新预测将来的一个月的股票信息
    upda = tk.Button(top, text='更新数据', width=10, height=2, font=('Arial', 12), command=update).place(x=500, y=10)
    start = tk.Button(top, text='开始预测', width=10, height=2, font=('Arial', 12), command=startyuce).place(x=500, y=110)
    start_test = tk.Button(top, text='开始验证', width=10, height=2, font=('Arial', 12), command=startyanzhen).place(x=500, y=210)

    # 打印出结预测结果
    textPad = ScrolledText(top, width=100, height=30, font=('Arial', 12))
    textPad.place(x=0, y=300)

    # 验证
    def yanzheng(name, N):
        if os.path.exists('../model/'+name+'.h5'):

            start2 = datetime.datetime(2019, 4, 1)
             # 真实数据集合
            if os.path.exists('./data/Test/'+name+'_Test.csv'):
                dataset_Test = pd.read_csv('./data/Test/'+name+'_Test.csv')
            else:
                dataset_Test = pdr.get_data_yahoo(name, start=start2, end=datetime.datetime.now())
                dataset_Test.to_csv('./data/Test/'+name+'_Test.csv')

            predicted_stock_price=forecast(name,N)

            print(predicted_stock_price)

            test_set=dataset_Test['Open']
            test_set=test_set[0:int(N)]
            print(test_set)
            test_set = pd.DataFrame(test_set)
            Table = test_set
            Table["predicted_stock_price"] = predicted_stock_price
            Table.columns = ['real_stock_price', 'predicted_stock_pric']
            print("-----------------------")
            plt.plot(Table['real_stock_price'], color='red', label='Real' + name + 'tock Price')
            plt.plot(Table['predicted_stock_pric'], color='blue', label='Predicted' + name + ' Stock Price')
            plt.xticks(range(0,int(N),1))
            plt.title(name + ' Stock Price Prediction Check')
            plt.xlabel('Time')
            plt.ylabel(name + ' Stock Price')
            plt.legend()
            plt.show()

            Table['error'] = Table['real_stock_price'] - Table['predicted_stock_pric']
            print(type(Table))
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(Table))


    # 预测
    def forecast(name, N):
        if os.path.exists('../model/' + name + '.h5'):
            regressor = load_model('../model/' + name + '.h5')
            dataset = pd.read_csv('./data/Train/' + name + '_Train.csv', index_col="Date", parse_dates=True)
            Test_set=dataset['Open']
            first_set=Test_set[len(Test_set)-60:]
            sc = MinMaxScaler(feature_range=(0, 1))  #归一化
            testing_set = pd.DataFrame(first_set)
            inputs = sc.fit_transform(testing_set)

            for i in range(60,60+int(N)):
                X_test = []
                X_test.append(inputs[i - 60:i, 0])
                X_test = X_test[0:60]
                X_test = np.array(X_test)
                X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
                prepricetest = regressor.predict(X_test)  # 预测结果
                inputs=np.vstack((inputs, prepricetest))


            preprice=inputs[len(inputs)-int(N):len(inputs),0]

            preprice=np.array(preprice)
            preprice=preprice.reshape(len(preprice), 1)

            preprice = sc.inverse_transform(preprice)

            plt.plot(preprice, color='blue', label='Predicted' + name + ' Stock Price')
            plt.xticks(range(0,len(preprice),1))

            plt.title(name + ' Stock Price Prediction')
            plt.xlabel('Time')
            plt.ylabel(name + ' Stock Price')
            plt.legend()
            plt.show()
            preprice1=preprice
            Table=pd.DataFrame(preprice,index=range(1,len(preprice)+1,1),columns=['Stock Price'])
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(Table))
            print(type(preprice))
            return preprice1  # 返回预测值



# 预测家公司当前的股票
def update():
    now_time = datetime.datetime.now()
    print(now_time)
    delta = datetime.timedelta(days=45)
    n_days=now_time-delta
    print(n_days)


def test():
    pass

if __name__ == '__main__':
   pass