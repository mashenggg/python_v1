#-*- coding:utf-8 -*-
# import movies as movies
import requests
import os
import time
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import re
import numpy as np

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    # "Referer": "https://movie.douban.com/",
    "Referer": "https://cd.lianjia.com/ershoufang/longquanyi/",
    'User-Agent': userAgent
}
longquan_txt=open("longquan.txt", 'w', encoding='utf-8')
test=[]
def yangguangc():
    for i in range(100):
        url = 'https://cd.lianjia.com/ershoufang/longquanyi/pg{}/'.format(i+1)
        data=requests.get(url,headers=header).text
        soup = BeautifulSoup(data,'lxml')
        li = soup.find_all('li',class_='clear LOGCLICKDATA')
        for o in li:
            div=o.find_all('div',attrs={'class':'info clear'})
            # print(div)
            for p in div:
                name=p.find('a',attrs={'target':'_blank'}).string
                price=p.find('div',class_='totalPrice').span.string
                xiaoquname=p.find('',attrs={'data-el':'region'}).string
                area = p.find('div',class_='houseInfo').text[15:22]
                introduce=p.find('div',class_='houseInfo').text
                UnitPrice=p.find('div',class_='unitPrice').span.string
                gg = re.sub("\D", "", UnitPrice)  #将单价转换为纯数字，提取当中的数字
                # print(xiaoquname)
                # print(type(area))
                # print(area)
                # print(introduce)
                # print(name)
                # print(price)
                # print(UnitPrice)
                # print(gg)
                test.append(gg)

                longquan_txt.write("发布名称:{}，价格:{},小区名称:{},面积:{},简介:{},单价:{} '\n'".format(name,price,xiaoquname,area,introduce,UnitPrice))
                # 将数据存入数据库
                # db = pymysql.connect(host='122.112.202.145', user='root', password='123456', port=3306)
                # cursor = db.cursor()  # 获取游标
                #
                # sql = 'replace into lianjia.longquan(name,price,xiaoquname,area,introduce,UnitPrice) values (%s,%s,%s,%s,%s,%s)'
                # try:
                #     cursor.execute(sql, (name,price,xiaoquname,area,introduce,UnitPrice))
                #     db.commit()
                # except:
                #     db.rollback()
                # db.close()
                # time.sleep(1)
yangguangc()


#求平均值
def pingjun():
    gg=list(map(int, test)) #转为int
    average=np.mean(gg) #求平均值
    print(average)
pingjun()
