# run.py 用于显示界面和调用其他程序

# 导入库函数
import tkinter as tk
import subprocess
import tkinter.messagebox as messagebox
import ctypes
import os

# 设置DPI_AWARE选项以提高清晰度
ctypes.windll.shcore.SetProcessDpiAwareness(1)


# 按钮一功能函数：运行爬虫文件
def run_script1():
    try:
        result = subprocess.run(["python", "crawler.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode == 0:
            messagebox.showinfo("运行成功", "数据读取成功！")
        else:
            messagebox.showerror("运行失败", "数据读取失败！")
    except Exception as e:
        messagebox.showerror("运行错误", str(e))


# 按钮三功能函数：运行预测股票文件
def run_script2():
    try:
        subprocess.run(["python", "forecast.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        messagebox.showerror("运行错误", str(e))


# 按钮二功能函数：打开爬虫爬取数据的所在文件夹
def open_output_folder():
    output_folder = "output"
    if os.path.exists(output_folder):
        subprocess.Popen(["explorer", output_folder], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        messagebox.showwarning("警告", "找不到output文件夹！")


# 创建主窗口
root = tk.Tk()
root.title("股票分析程序 Ver0.8 byPC")
root.geometry("600x520")

# 添加标题标签
title_label = tk.Label(root, text="欢迎使用股票分析程序", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

# 创建按钮
button1 = tk.Button(root, text="点击查询", font=15, command=run_script1)
button1.grid(row=1, column=0, padx=18, pady=12)
button2 = tk.Button(root, text="打开文件", font=15, command=open_output_folder)
button2.grid(row=1, column=1, padx=18, pady=12)
button3 = tk.Button(root, text="点击预测", font=15, command=run_script2)
button3.grid(row=1, column=2, padx=18, pady=12)

# 设置按钮样式
button1.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button2.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))
button3.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))

# 添加标签语句
label1 = tk.Label(root, text="请依次单击按钮运行使用\n出现预览，确认无误后关闭窗口即可\n\n"
                             "功能介绍：\n"
                             "1.点击查询：获取股票数据，并保存在output文件夹中\n"
                             "2.打开文件：打开output文件夹以检查爬取的股票数据\n"
                             "3.点击预测：绘制股票曲线图并股票进行预测\n"
                             "4.请确保output文件夹中存在有效文件再进行预测\n"
                             "5.目前该版本相关设置参数如 选择爬取数据的日期、\n"
                             "预测数据的对象 需在源代码中修改", font=("Helvetica", 12))
label1.grid(row=2, column=0, columnspan=3, padx=20, pady=10)
label2 = tk.Label(root, text="请注意！目前本程序预测范围有限且误差范围较大\n"
                             "无法完全作为股票购买的依据，仅供参考学习使用", fg="red", font=("Helvetica", 12))
label2.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

# 启动图形化界面
root.mainloop()
