#-*- coding:utf-8 -*-
# import movies as movies
import requests
import sys
import os
import time
import http.cookiejar as cookielib
print(f"user cookielib in python3.")
from lxml import etree
import pymysql
#cookie
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "https://movie.douban.com/",
    # "Referer": "https://www.douban.com/",
    # "Host":"accounts.douban.com",
    'User-Agent': userAgent
}
doubanSession = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
doubanSession.cookies = cookielib.LWPCookieJar(filename = "doubanCookies.txt")
def doubanwoLogin(account, password):
    # 模仿 登录
    print ("开始模拟豆瓣网")

    postUrl = "https://accounts.douban.com/passport/login?source=movie"
    # postUrl = "https://accounts.douban.com/passport/login_popup?login_source=anony"
    postData = {
        "username": account,
        "password": password,
    }
    # 使用session直接post请求
    responseRes = doubanSession.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
    doubanSession.cookies.save()
doubanwoLogin("15928636408", "qad259885")
#设置douban文本全局变量
douban_txt=open("豆瓣电影250.txt", 'w', encoding='utf-8')
def douban():
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25) #总共10页，用 i*25 保证已25为单位递增
        data = doubanSession.get(url,headers = header,allow_redirects = False).text#使用get方法发送请求，返回网页数据的Response并存储到对象data 中
        # print(data)
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

            # sql = 'insert into douban.douban_movie(movie_name,movie_pingfen,movie_pingjia,movie_brief) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE movie_name = %s, movie_pingfen = %s, movie_pingjia = %s,movie_brief = %s'
            sql = 'replace into douban.douban_movie(movie_name,movie_pingfen,movie_pingjia,movie_brief) values (%s,%s,%s,%s)'

            try:
                cursor.execute(sql, (movie_name, movie_pingfen, movie_pingjia, movie_brief))
                db.commit()
            except:
                db.rollback()
            db.close()
            #存入本地txt文本
            douban_txt.write("电影名称:{}——电影评分:{}——评价人数:{}——简介:{} + '\n'".format(movie_name,movie_pingfen,movie_pingjia,movie_brief))

douban()