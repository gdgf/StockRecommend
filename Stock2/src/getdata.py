import os
import pandas_datareader as pdr
import datetime


start1 = datetime.datetime(2014,1,1)
end1   = datetime.datetime(2019,3,31)

start2 = datetime.datetime(2019,4,1)
now=   datetime.datetime.now()
path="./data/Train/"

# 获取股票数据
def getdata(name):
    print('开始获取数据!\n')
    filelist=get_name(path)
    file=name+"_Train.csv"
    if file in filelist: #数据集已经存在
        pass
    else:
       data1 = pdr.get_data_yahoo(name, start=start1, end=end1)
       data2=pdr.get_data_yahoo(name, start=start2, end=now)
       data1.to_csv("./data/Train/"+name+"_Train.csv")
       data2.to_csv("./data/Test/" + name + "_Test.csv")

    print("获取数据成功！\n")

# 得到文件夹下所有文件的名字
def get_name(dir):
    all_files = []
    filenames = os.listdir(dir)
    # 得到带有路径的文件名
    for filename in filenames:
        p = os.path.join(filename)
        if p.endswith('.csv'):
            all_files.append(p)
    return all_files