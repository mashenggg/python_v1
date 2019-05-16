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
douban_txt=open("豆瓣一周口碑榜.txt", 'w', encoding='utf-8')

def douban_week():
    url = 'https://movie.douban.com/'
    data = doubanSession.get(url,headers = header,allow_redirects = False).text
    # print(data)
    m = etree.HTML(data)
    week=m.xpath('//*[@id="billboard"]/div[2]')
    for i in week:
        movie_name = i.xpath('./table/tr/td[2]/a/text()')[0:9]
        # print(movie_name)
        # print(type(movie_name))
        # print(movie_name[0])
        for o in movie_name:
            # print(o)
            douban_txt.write("电影名称：{} '\n'".format(o))
douban_week()