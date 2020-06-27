#作业一：
#安装并使用 requests、bs4 库，
#爬取猫眼电影的前 10 个电影名称、电影类型和上映时间
#以 UTF-8 字符集保存到 csv 格式的文件中。

import requests
from bs4 import BeautifulSoup as bs

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"

header = {}
header['user-agent'] = user_agent

myurl = "https://maoyan.com/board/4"

response = requests.get(myurl,headers=header)

print(response.text)
print(f'返回码是：{response.status_code}')

#用html.pares方式解析
bs_info = bs(response.text,'html.parser') #用html.pares方式解析

#用于存数据
mylist = []

# Python 中使用for in 形式的循环，Python使用缩进来做语句分隔
for tags in bs_info.find_all('div',attrs={'class':'movie-item-info'}):
    data = []
    for atag in tags.find_all('a',):
        #获取所有链接
        #print(atag.get('href'))
        data.append ('https://maoyan.com' + str(atag.get('href')))
        #获取影片名
        #print(atag.get('title'))
        data.append(atag.get('title')) 
    for atagtime in tags.find_all('p',attrs={'class':'releasetime'}):
        #获取上映时间
        #print(atagtime.text)
        data.append(atagtime.text)
    #将取到的第一条记录加入到列表
    mylist.append(data)

#打印调试
print(mylist)

#写入表
import pandas as pd
movie1 = pd.DataFrame(data=mylist)

movie1.to_csv('./week01/movie_work01.csv',encoding='utf8',index=False,header=False)



    
