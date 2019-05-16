#-*- coding:utf-8 -*-
# import movies as movies
import requests
import sys
import os
import time
from lxml import etree
import pymysql
# douban_txt=open("豆瓣电影250.txt", 'w+', encoding='utf-8')
def douban():
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25) #总共10页，用 i*25 保证已25为单位递增
        data = requests.get(url).text#使用get方法发送请求，返回网页数据的Response并存储到对象data 中
        m = etree.HTML(data)##用etree.HTML 来解析变量data(页面数据)
        movie = m.xpath('//*[@id="content"]/div/div[1]/ol/li/div')        #定位到主盒子
        for div in movie:
            movie_name = div.xpath('./div[2]/div[1]/a/span[1]/text()')[0]
            movie_pingfen = div.xpath('./div[2]/div[2]/div/span[2]/text()')[0]
            movie_pingjia = div.xpath('./div[2]/div[2]/div/span[4]/text()')[0]
            movie_brief = div.xpath('./div[2]/div[2]/p[2]/span/text()')
            # print ("电影名称{}——电影评分:{}——评价人数:{}——简介:{}".format(movie_name,movie_pingfen,movie_pingjia,movie_brief))
            # return movie_name,movie_pingfen,movie_pingjia,movie_brief
            #将数据存入数据库
            db = pymysql.connect(host='192.168.100.29', user='root', password='ms123456', port=3306)
            cursor = db.cursor()  # 获取游标
            sql = 'insert into douban.douban_movie(movie_name,movie_pingfen,movie_pingjia,movie_brief) values (%s,%s,%s,%s)'
            try:
                cursor.execute(sql, (movie_name, movie_pingfen, movie_pingjia, movie_brief))
                db.commit()
            except:
                db.rollback()
            db.close()
            #存入本地txt文本
douban()
# db = pymysql.connect(host='192.168.100.29',user='root', password='ms123456', port=3306)
# cursor = db.cursor()#获取游标
# sql='CREATE TABLE douban.douban_movie (id INT(50) not null,movie_name VARCHAR(100) not null,movie_pingfen VARCHAR(100),movie_pingjia VARCHAR(100),movie_brief VARCHAR( 100 ),PRIMARY key( id ))'
# sql='insert into douban.douban_movie(movie_name,movie_pingfen,movie_pingjia,movie_brief) values (%s,%s,%s,%s)'
# try:
    # cursor.execute(sql,(movie_name,movie_pingfen,movie_pingjia,movie_brief))
    # db.commit()
# except:
#     db.rollback()
# data = cursor.fetchall()
# print(data)
# db.close()