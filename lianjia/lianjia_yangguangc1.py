#-*- coding:utf-8 -*-
import json
import requests
import os
import time
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import numpy as np
import re
import pymongo
import xlwt

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    # "Referer": "https://movie.douban.com/",
    "Referer": "https://cd.lianjia.com/ershoufang/yangguangcheng/",
    'User-Agent': userAgent
}
yangguangcheng_txt=open("yangguangcheng.txt", 'w', encoding='utf-8')
test=[]
def yangguangc():
    for i in range(yeshu):
        url = 'https://cd.lianjia.com/ershoufang/yangguangcheng/pg{}/'.format(i+1)
        data=requests.get(url,headers=header).text
        soup = BeautifulSoup(data,'lxml')
        li = soup.find_all('li',class_='clear LOGCLICKDATA')
        info={}
        for o in li:
            div=o.find_all('div',attrs={'class':'info clear'})
            # print(type(div))
            for p in div:
                info["名称"]= p.find('a',attrs={'target':'_blank'}).text
                info["总价"] =p.find('div',class_='totalPrice').text
                info["小区名称"] =p.find('',attrs={'data-el':'region'}).text
                info["面积"] =p.find('div',class_='houseInfo').text[15:22]
                info["简介"] =p.find('div',class_='houseInfo').text
                info["单价"] =p.find('div',class_='unitPrice').span.text
                print(type(info))
                name=info['名称']
                price=info['总价']
                xiaoquname=info['小区名称']
                area=info['面积']
                introduce=info['简介']
                UnitPrice=info['单价']

                info_new = ({
                    'name':name,
                    'price':price,
                    'xiaoquname':xiaoquname,
                    'area':area,
                    'introduce':introduce,
                    'UnitPrice':UnitPrice
                })

                # 将单价转为数字存放在test列表
                UnitPrice = info['单价']
                gg = re.sub("\D", "", UnitPrice)  # 提取数字
                test.append(gg)  # 将单价添加为列表

                #存入txt文本
                # yangguangcheng_txt.write(json.dumps("{}" '\n'.format(info)))
                yangguangcheng_txt.write("{}" '\n'.format(info))
                # yangguangcheng_txt.write("发布名称:{}，价格:{},小区名称:{},面积:{},简介:{},单价:{} '\n'".format(name,price,xiaoquname,area,introduce,UnitPrice))


                # 将数据存入数据库
                db = pymysql.connect(host='122.112.202.145', user='root', password='123456', port=3306)
                cursor = db.cursor()  # 获取游标

                sql = 'replace into lianjia.yangguangcheng(name,price,xiaoquname,area,introduce,UnitPrice) values (%s,%s,%s,%s,%s,%s)'
                try:
                    cursor.execute(sql, (name,price,xiaoquname,area,introduce,UnitPrice))
                    db.commit()
                    print("存储mysql成功")
                except:
                    db.rollback()
                    print("存储mysql失败")
                db.close()

                #存入mongo
                client = pymongo.MongoClient(host='122.112.202.145', port=27017)
                db = client.lianjia
                collection = db.yangguangcheng
                result = collection.insert_one(info_new)
                print("存储mongo成功")
# 求平均值
def pingjun():
    gg=list(map(int, test)) #转为int
    average=np.mean(gg) #求平均值
    print(average)
    yangguangcheng_txt.write("平均价格为:{}".format(average))

if __name__ == '__main__':
    yeshu=int(input("输入页数"))

yangguangc()
pingjun()