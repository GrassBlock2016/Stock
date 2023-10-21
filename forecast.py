# forecast.py 用于RNN模型学习预测

"""
# 导入库函数
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import model_selection
from sklearn import metrics

# 读取文件赋值X和y
stock = pd.read_excel
X = stock.iloc
y = stock.iloc

# 切分数据集为训练集和测试集
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.35,random_state=1)
linreg = LinearRegression()
linreg.fit(X_train,y_train)
y_test_pred = linreg.predict(X_test)
y_test_err = metrics.mean_squared_error(y_test,y_test_pred)
predict_score = linreg.score(X_test,y_test)

# 输出预测结果
new_X =
new_y = linreg.predict(new_X)
print(new_y)
"""

# 以上为机器学习的方法，由于误差过高故采用以下RNN的方法

# 导入库函数
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import ctypes
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN

# 设置DPI_AWARE选项以提高清晰度
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 创建窗口
root = tk.Tk()
root.title("数据预测(拟合)")

# 添加标题标签
title_label = tk.Label(root, text="请选择要预测(拟合)的数据\n"
                                  "当前版本仅支持以下数据的拟合", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

# 读取文件
data1 = pd.read_csv('output//谷歌.csv', sep=',')
data2 = pd.read_csv('output//亚马逊.csv', sep=',')
data3 = pd.read_csv('output//苹果.csv', sep=',')
data4 = pd.read_csv('output//Facebook.csv', sep=',')
data5 = pd.read_csv('output//阿里巴巴.csv', sep=',')
data6 = pd.read_csv('output//腾讯.csv', sep=',')
data = None


# 定义提取X和y的函数
def extractdata(data, time_step):
    X = []
    y = []
    for i in range(len(data) - time_step):
        X.append([a for a in data[i:i + time_step]])
        y.append(data[i + time_step])
    X = np.array(X)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    return X, y


# 定义选项函数
def forecast_data(new_data):
    global data
    data = new_data
    time_step = 8

    # 归一化处理
    price = data.loc[:, 'Close']
    price_norm = price / max(price)

    # 定义X和y
    X, y = extractdata(price_norm, time_step)
    X = np.array(X)
    y = np.array(y)

    """
    # 作图
    fig1 = plt.figure(figsize=(8, 5))
    plt.plot(price)
    plt.title('Close Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()
    """

    # 建立RNN模型
    model = Sequential()
    model.add(SimpleRNN(units=5, input_shape=(time_step, 1), activation='relu'))
    model.add(Dense(units=1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(X, y, batch_size=30, epochs=200)

    # 预测
    y_train_predict = model.predict(X) * max(price)
    y_train = [i * max(price) for i in y]

    # 再次作图
    fig2 = plt.figure(figsize=(8, 5))
    plt.plot(y_train, label='True Price')
    plt.plot(y_train_predict, label='Predict Price')
    plt.title('Close Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


# 创建选项
button1 = tk.Button(root, text="谷   歌", command=lambda: forecast_data(data1), font=("Helvetica", 12))
button1.grid(row=1, column=0, columnspan=3, padx=20, pady=10)
button1.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button2 = tk.Button(root, text="亚马逊", command=lambda: forecast_data(data2), font=("Helvetica", 12))
button2.grid(row=2, column=0, columnspan=3, padx=20, pady=10)
button2.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button3 = tk.Button(root, text="苹   果",  command=lambda: forecast_data(data3), font=("Helvetica", 12))
button3.grid(row=3, column=0, columnspan=3, padx=20, pady=10)
button3.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button4 = tk.Button(root, text="脸   书", command=lambda: forecast_data(data4),  font=("Helvetica", 12))
button4.grid(row=4, column=0, columnspan=3, padx=20, pady=10)
button4.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button5 = tk.Button(root, text="阿   里", command=lambda: forecast_data(data5),  font=("Helvetica", 12))
button5.grid(row=5, column=0, columnspan=3, padx=20, pady=10)
button5.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button6 = tk.Button(root, text="腾   讯", command=lambda: forecast_data(data6),  font=("Helvetica", 12))
button6.grid(row=6, column=0, columnspan=3, padx=20, pady=10)
button6.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))

# 启动主事件循环
root.mainloop()
