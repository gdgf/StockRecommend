import os
import tkinter as tk  # 使用Tkinter前需要先导入
from matplotlib.pylab import mpl

ARTICLE_DIR = '../data/base'

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


# 得到文件夹下所有文件的名字
def get_name(dir):
    all_files = []
    filenames = os.listdir(dir)
    # 得到带有路径的文件名
    for filename in filenames:
        p = os.path.join(filename)
        if p.endswith('.txt'):
            all_files.append(p)
            print(p)
    return all_files


def Information():
    top = tk.Toplevel()
    top.title('资讯')
    top.geometry('1000x500')  # 这里的乘是小x
    v1 = tk.StringVar()

    list_items = get_name(ARTICLE_DIR)
    lb = tk.Listbox(top, listvariable=v1, font=('Arial', 12))

    for item in list_items:
        lb.insert('end', item)
    lb.grid(row=1, column=1, padx=10)

    e = tk.Text(top, show=None, font=('Arial', 12))  # 显示成明文形式
    e.grid(row=1, column=2)

    def print_selection():
        value = lb.get(lb.curselection())  # 获取当前选中的文本
        filename = os.path.join(ARTICLE_DIR, value)
        with open(filename, encoding='utf-8') as sentence:
            content = sentence.read()
            e.delete(1.0, tk.END)
            e.insert('end', content,)  # 为label设置值

    b1 = tk.Button(top, text='print selection', width=15, height=2, command=print_selection)
    b1.grid(row=2, column=2, pady=10)
