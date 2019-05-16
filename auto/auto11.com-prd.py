#-*- coding:utf-8 -*-
# import movies as movies
import requests
import sys
import os
import time
from lxml import etree
import pymysql
from bs4 import BeautifulSoup

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    # "Referer": "https://movie.douban.com/",
    "Referer": "https://www.auto11.com/index.aspx",
    'User-Agent': userAgent
}
auto_txt=open("auto.txt", 'w', encoding='utf-8')
def auto11():
    for h in range(3):
        url = 'https://www.auto11.com/products/3-0-{}.html#meizz'.format(h+1)
        data=  requests.get(url,headers=header).text
        soup = BeautifulSoup(data,'lxml')
        # Soup=print(soup.prettify())
        # print(Soup)
        # print(soup.title.string)
        div = soup.find_all('div',class_='rt_li') #找到主盒子
        for i in div:
            div_data=(i.find_all('ul'))
            for o in div_data:
                shangpin_name = (o.find(name='a', attrs={'target': '_blank'})).text
                price_data=(o.find(name='span', class_='font14 fontB colore4393c fmlyari')).text
                # name=(shangpin_name['title'])
                print(price_data)
                print(shangpin_name)

                #存入文本
                auto_txt.write("商品名称：{},商品价格：{} '\n'".format(shangpin_name,price_data))
                # 将数据存入数据库
                # db = pymysql.connect(host='192.168.100.29', user='root', password='ms123456', port=3306)
                # cursor = db.cursor()  # 获取游标
                #
                # sql = 'replace into auto11.auto_shangpin(name,jiage) values (%s,%s)'
                # try:
                #     cursor.execute(sql, (name,price_data))
                #     db.commit()
                # except:
                #     db.rollback()
                # db.close()
auto11()
