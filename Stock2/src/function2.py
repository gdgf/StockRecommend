import re,os
import pandas as pd
import tushare as ts
import tkinter as tk
import tkinter.messagebox  # 要使用messagebox先要导入模块
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt

from  src.others import getdrop,getrise

data = pd.DataFrame()

# main
def StockRecommendation():
    top = tk.Toplevel()
    top.title('股票推荐与分析')
    top.geometry('1000x800')  # 这里的乘是小x

    # 获得股票信息，并加以整理，计算
    def get_data():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data))
            tkinter.messagebox.showinfo(title='Hi', message='初始化完成')  # 提示信息对话窗
        else:
            data_code = pd.DataFrame()
            code = ts.get_hs300s().code
            # 1.股票代码
            data_code['code'] = code
            print("股票代码：\n", data_code.head())
            # 2. 获取衡量获利能力的指标数据 ,第一季度数据
            profit = ts.get_profit_data(2019, 1)
            profit = profit[['code', 'name', 'net_profit_ratio']]
            data_profit = pd.merge(data_code, profit, on='code')
            print("股票获利能力\n", data_profit.head())
            # 3. 计算获取沪深300的股价波动幅度数据
            data_change = pd.DataFrame()
            for co in data_profit.code:
                # 获取月K线数据333
                change = ts.get_hist_data(co, start='2019-01-01', end='2019-03-31', ktype='M')
                change['p_undulate'] = (change['high'] - change['low']) / change['low']
                change = change[['p_undulate']]
                var1 = change.sum()  # 计算总波动
                var1['code'] = co
                data_change = pd.concat([data_change, var1], axis=1, sort=False)
            data_change = data_change.T  # 转置
            print("股价波动：\n", data_change.head())

            # 4. 股票市场性质
            # 以流动股本/总股本来表征股票市场性
            # 从基本表中获取流动股本和总股本数据
            market = ts.get_stock_basics()
            market = market[['outstanding', 'totals']]
            market['turnover_rate'] = market['outstanding'] / market['totals']
            market = market[['turnover_rate']]
            data_market = pd.merge(data_code, market, on='code')
            print("股票市场性：\n", data_market.head())
            # 5. 运营能力
            operation = ts.get_operation_data(2019, 1)
            operation = operation[['code', 'currentasset_turnover']]
            data_operation = pd.merge(data_code, operation, on='code')
            print("运营能力：\n", data_operation.head())

            # 6. 短期偿债能力
            debtpaying = ts.get_debtpaying_data(2019, 1)
            debtpaying = debtpaying[['code', 'currentratio']]
            data_debtpaying = pd.merge(data_code, debtpaying, on='code')
            print("短期偿债能力：\n", data_debtpaying.head())

            # 7. 财务结构
            financial = ts.get_debtpaying_data(2019, 1)
            financial = financial[['code', 'sheqratio']]
            data_financial = pd.merge(data_code, financial, on='code')
            print("财务结构：\n", data_financial.head())

            # 8.将多个数据集合并为一个
            data = data_profit.merge(data_change, on='code').merge(data_market, on='code').merge(data_operation,on='code') \
                 .merge(data_debtpaying, on='code').merge(data_financial, on='code')
            print("整合数据：\n", data.head())

            # 10.将非数字的值替换为零
            def format(x):
                value = re.compile(r'^\s*[-+]*[0-9]+\.*[0-9]*\s*$')
                # 不是数字
                if value.match(str(x)):
                    return float(x)
                else:
                    return 0

            data['net_profit_ration'] = data['net_profit_ratio'].apply(format)
            data['sheqration'] = data['sheqratio'].apply(format)
            data['currentasset_turnover'] = data['currentasset_turnover'].apply(format)
            data['currentratio'] = data['currentratio'].apply(format)
            print("非数字替换：\n", data.head())

            # 11.计算股票得分
            print("计算得分：\n")
            data['score'] = data['net_profit_ratio'] * 0.4 + data['p_undulate'] * 100 * 0.2 + data[
                'turnover_rate'] * 100 * 0.15 \
                            + data['currentasset_turnover'] * 100 * 0.15 + data['currentratio'] * 100 * 0.05 + \
                            data['sheqratio'] * 0.05

            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data))
            data.to_csv("./data/data.csv")
            tkinter.messagebox.showinfo(title='Hi', message='初始化完成')  # 提示信息对话窗


    # 手动显示数据
    def readdata():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")

            if os.path.exists("./data/data.csv"):
                data = pd.read_csv("./data/data.csv")
                data['score'].plot()
                plt.xlabel('code')
                plt.ylabel('score')
                plt.title("Score")
                plt.show()
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data))
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))

    # 根据得分推荐
    # 强力买入
    def one():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            data1 = data[data.score >= 100]
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data1))
            mes = str(data1['name'])
            tkinter.messagebox.showinfo(title='强力推荐买入', message=mes)  # 提示信息对话窗
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))
    # 买入
    def two():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            data2 = data[(data.score < 100) & (data.score >= 75)]
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data2))
            mes = str(data2['name'])
            tkinter.messagebox.showinfo(title='推荐买入', message=mes)  # 提示信息对话窗
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))

    # 观望
    def three():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            data3 = data[(data.score < 75) & (data.score >= 50)]
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data3))
            mes = str(data3['name'])
            tkinter.messagebox.showinfo(title='推荐观望', message=mes)  # 提示信息对话窗
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))

    # 适度减持
    def four():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            data4 = data[(data.score < 50) & (data.score >= 25)]
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data4))
            mes = str(data4['name'])
            tkinter.messagebox.showinfo(title='适度减持', message=mes)  # 提示信息对话窗
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))
    # 买出
    def five():
        if os.path.exists("./data/data.csv"):
            data = pd.read_csv("./data/data.csv")
            data5 = data[data.score < 25]
            textPad.delete(1.0, tk.END)
            textPad.insert(tkinter.constants.END, chars=str(data5))
            mes = str(data5['name'])
            tkinter.messagebox.showinfo(title='推荐买出', message=mes)  # 提示信息对话窗
        else:
            data = " "
            textPad.insert(tkinter.constants.END, chars=str(data))

    # 计算预测准确性
    def checking():
         if os.path.exists("./data/4pchange.csv"):
              pchange4= pd.read_csv("./data/4pchange.csv")
         else:
             data_code = pd.DataFrame()
             code = ts.get_hs300s().code
             data_code['code'] = code
             # 1.股票代码
             pchange = pd.DataFrame()
             for code in data_code.code:
                 da = ts.get_hist_data(code, start='2019-03-31', end='2019-04-30', ktype="M")
                 da = da[['p_change']].mean()
                 da['code'] = code
                 pchange = pd.concat([pchange, da], axis=1, sort=False)
             pchange4=pchange.T
             # 4月份数据改变
             pchange4.to_csv("./data/4pchange.csv")


         textPad.delete(1.0, tk.END)
         data=pd.read_csv("./data/data.csv")
         data1=data[data.score >= 100]
         data1 = pchange4.merge(data1[['code', 'score']], on='code')
         str1="强力推荐买入 上涨股票占比：{:.2%}\n".format(getrise(data1))
         textPad.insert(tkinter.constants.END, chars=str(str1))

         data2 = data[(data.score < 100) & (data.score >= 75)]
         data2 = pchange4.merge(data2[['code', 'score']], on='code')
         str2 = "推荐买入 上涨股票占比：{:.2%}\n".format(getrise(data2))
         textPad.insert(tkinter.constants.END, chars=str(str2))

         data3 = data[(data.score < 75) & (data.score >= 50)]
         data3 = pchange4.merge(data3[['code', 'score']], on='code')
         str3 = "推荐观望 上涨股票占比：{:.2%}\n".format(getrise(data3))
         textPad.insert(tkinter.constants.END, chars=str(str3))


         data4 = data[(data.score < 50) & (data.score >= 25)]
         data4 = pchange4.merge(data4[['code', 'score']], on='code')
         str4 = "推荐适度减持 下跌股票占比：{:.2%}\n".format(getdrop(data4))
         textPad.insert(tkinter.constants.END, chars=str(str4))

         data5 = data[data.score < 25]
         data5 = pchange4.merge(data5[['code', 'score']], on='code')
         str5 = "推荐买出 下跌股票占比：{:.2%}\n".format(getdrop(data5))
         textPad.insert(tkinter.constants.END, chars=str(str5))



    btn_login = tk.Button(top, text='初始化数据', width=12, height=2, font=('Arial', 12),command=get_data)
    btn_login.grid(row=1, column=1, padx=30, pady=20)
    b1 = tk.Button(top, text='股票得分', width=15, height=2, font=('Arial', 12), command=readdata)
    b1.grid(row=1, column=2, padx=30, pady=20)
    btn_sign_up = tk.Button(top, text='准确率验证', width=12, height=2,font=('Arial', 12), command=checking)
    btn_sign_up.grid(row=1, column=3, padx=30, pady=10)

    textPad = ScrolledText(top, width=80, height=40,font=('Arial', 12))
    textPad.place(x=0, y=100)


    tk.Label(top, text='股票推荐', font=('Arial', 12)).place(x=800, y=200)
    first = tk.Button(top, text='强力推荐买入', width=15, height=2, font=('Arial', 12),command=one)
    first.place(x=800, y=300)
    second = tk.Button(top, text='推荐买入', width=15, height=2, font=('Arial', 12),command=two)
    second.place(x=800, y=400)
    third = tk.Button(top, text='推荐观望', width=15, height=2, font=('Arial', 12),command=three)
    third.place(x=800, y=500)
    fouth = tk.Button(top, text='推荐适度减持', width=15, height=2, font=('Arial', 12),command=four)
    fouth.place(x=800, y=600)
    fifth = tk.Button(top, text='推荐卖出', width=15, height=2, font=('Arial', 12),command=five)
    fifth.place(x=800, y=700)


def test():
    pass

