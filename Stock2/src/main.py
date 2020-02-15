import tkinter as tk  # 使用Tkinter前需要先导入

from src.function1 import Information
from src.function2 import StockRecommendation
from src.function3 import Forecast

window = tk.Tk()
window.title('股票推荐系统')
window.geometry('600x300')  # 这里的乘是小x


canvas = tk.Canvas(window, width=400, height=135, bg='green')
image_file = tk.PhotoImage(file='../data/pic/pic.gif')
image = canvas.create_image(200, 0, anchor='n', image=image_file)  # 图片绘制在canvas上
canvas.pack(side='top')
tk.Label(window, text='Wellcome', font=('Arial', 13)).pack()

btn_login = tk.Button(window, text='资讯',width=12, height=2, font=('Arial', 12), command=Information)
btn_login.place(x=50, y=200)


btn_sign_up = tk.Button(window, text='股票分析与推荐',width=12, height=2,font=('Arial', 12),command=StockRecommendation)
btn_sign_up.place(x=200, y=200)


btn_sign_up = tk.Button(window, text='个别股票预测', width=12,font=('Arial', 12),height=2,command=Forecast)
btn_sign_up.place(x=350, y=200)


btn_sign_up = tk.Button(window, text='退出', width=10, height=1, font=('Arial', 10),command=window.quit)
btn_sign_up.place(x=450, y=270)

window.mainloop()
