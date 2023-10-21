# crawler.py 用于爬取数据

"""
# 导入库函数
import requests
from bs4 import BeautifulSoup
import re

# 模拟浏览器发送请求
kv = {'user-agent': 'Mozilla/5.0'}

# 获取网页信息
def getHTMLText(url,code='UTF-8'):
    try:
        r = requests.get(url,headers=kv,timeout = 30)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        r.encoding = code
        return r.text
    except:
        #print("获取资源失败")
        return ""

# 获得股票的信息列表
def getStockList(lst,stockURL):
#第一个参数表示列表保存的列表类型，存储了所有股票的信息，第二个参数是获得股票列表的URL网站
    html = getHTMLText(stockURL,'UTF-8')
    soup = BeautifulSoup(html,'html.parser')#解析页面
    a = soup.find_all('a')#找到所有的a标签
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"S[ZH]{6}",href)[0])
        except:
            continue

# 获得个股信息并储存，包括三个参数：1.保存所有股票的信息列表 2.获得股票信息的URL网站 3.将来要把信息存到文件的文件路径
def getStockInfo(lst,stockURL,fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock
        html = getHTMLText(url)
        try:
            if html == " ":
                continue
            infoDict = {}                   # 定义字典存储从当前页面中返回的所有个股信息
            soup = BeautifulSoup(html,'html.parser')
            stockInfo = soup.find('div',attrs={'class':'stock_top clearfix'})
            name = stockInfo.find_all(attrs={'class':'stock_title'})[0]
            infoDict.update({'股票名称':name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val         # 字典可以直接使用key=value，向字典中新增内容
            # 将相关信息保存在文件中
            with open(fpath,'a',encoding = 'utf-8') as f:
                f.write(str(infoDict)+'\n')
                # 增加进度条可看当前进度百分比
                count = count + 1
                print('\r当前完成进度：{:.2f}%'.format(count*100/len(lst)),end=" ")
        except:
            print('\r当前完成进度：{:.2f}%'.format(count * 100 / len(lst)),end=" ")
            continue

# 主函数
def main():
    stock_list_rul = 'https://hq.gucheng.com/gpdmylb.html'      # 获得股票列表的URL链接
    stock_info_rul = 'https://hq.gucheng.com/'                  # 获取股票信息的链接的主体部分
    output_file = 'data//StockInfo.txt'
    slist = []                                                  # 股票的信息定义成一个列表变量
    getStockList(slist,stock_list_rul)                          # 获得股票列表
    getStockInfo(slist,stock_info_rul,output_file)              # 根据股票列表，到相关网站获取股票信息，并存储在文件中

main()
"""

# 以上为根据HTML爬取的方法，由于现阶段主流股票网站均采用JS动态加载，故更换思路

# 导入库函数
import yfinance as yf
import tkinter as tk
import ctypes

# 设置DPI_AWARE选项以提高清晰度
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 定义股票代码字典
gadatadict = {'谷歌': 'GOOG', '亚马逊': 'AMZN', '苹果': 'AAPL', 'Facebook': 'FB', '阿里巴巴': 'BABA', '腾讯': '0700.hk'}

# 创建输入窗口
root = tk.Tk()
root.title("数据查询")

# 添加标题标签
title_label = tk.Label(root, text="请输入查询的起止时间\n"
                                  "输入样例(yyyy-mm-dd)", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

# 创建一个输入框
label1 = tk.Label(root, text="起始时间：", font=("Helvetica", 12))
label1.grid(row=1, column=0, padx=18, pady=12)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1, padx=18, pady=12)
label2 = tk.Label(root, text="终止时间：", font=("Helvetica", 12))
label2.grid(row=2, column=0, padx=18, pady=12)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=1, padx=18, pady=12)

# 定义起止时间
start = ''
end = ''


# 定义一个函数来获取值
def get_input():
    global start, end
    start = entry1.get()
    end = entry2.get()

    # 调用yfinance库函数获取数据
    GOOGdata = yf.download(gadatadict['谷歌'], start, end)
    AMZdata = yf.download(gadatadict['亚马逊'], start, end)
    APLdata = yf.download(gadatadict['苹果'], start, end)
    FBdata = yf.download(gadatadict['Facebook'], start, end)
    ALBBdata = yf.download(gadatadict['阿里巴巴'], start, end)
    TENdata = yf.download(gadatadict['腾讯'], start, end)

    # 保存数据
    GOOGdata.to_csv('output//谷歌.csv')
    AMZdata.to_csv('output//亚马逊.csv')
    APLdata.to_csv('output//苹果.csv')
    FBdata.to_csv('output//Facebook.csv')
    ALBBdata.to_csv('output//阿里巴巴.csv')
    TENdata.to_csv('output//腾讯.csv')

    root.destroy()


# 创建一个按钮，用于触发获取输入框内容的函数
get_button = tk.Button(root, text="点击查询", command=get_input,font=("Helvetica", 12))
get_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10)
get_button.configure(bg="#4CAF50", fg="white", font=("Helvetica", 14))

# 启动图形化界面
root.mainloop()
