# -*- coding: UTF-8 -*-
import requests
import http.cookiejar as cookielib
import re
from lxml import etree
from bs4 import BeautifulSoup
import json
import pymysql

ypzdw_shouye=open("ypzdw.txt", 'w', encoding='utf-8')
#数据库
db = pymysql.connect(host='122.112.202.145', user='root', password='123456', port=3306)
cursor = db.cursor()  # 获取游标

header={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer':'https://passport.ypzdw.com/login?tab=account'
}
ypzdwsession=requests.session()
ypzdwsession.cookies=cookielib.LWPCookieJar(filename='ypzdwcookie.txt')
#模拟登陆
def ypzdwlogin():
    posturl="https://passport.ypzdw.com/login"
    postData = {
        'fromReg':'false',
        # 'tab':'mobile',
        'defaultTab':'account',
        "username":'testcg1',
        "password":'testcg1',
        # 'mobilePhone':'15928636408',
        # 'password':'ms123456',
    }
    response=ypzdwsession.post(url=posturl,headers=header,data=postData)
    print(f"statusCode = {response.status_code}")
    ypzdwsession.cookies.save()
ypzdwlogin()

def ypzdw_shouye_cbhh():
    data=ypzdwsession.get(url=cbhhurl,headers=header,allow_redirects = False).text
    data1=data[46:-2]
    result = json.loads(data1) #转为json
    # print(result)
    # print(type(result))
    xinxi=result['data']#取出data中数据为list
    for i in xinxi:
        prices=i['price'] #取出price，dict
        name=i['basic'] #取出商品详情

        itemName = name['itemName'] #名称
        price=prices['lowPrice']    #促销价
        highPrice=prices['highPrice']   #原价
        factoryName=name['factoryName'] #生产厂商
        specification=name['specification'] #规格
        allowNumber=name['allowNumber'] #批号
        ypzdw_shouye.write("首页-常备好货-商品名称:{},促销价格:{},原价:{},生产厂商:{},规格:{},批号:{} '\n'".format(itemName,price,highPrice,factoryName,specification,allowNumber))
        # print("首页-常备好货-商品名称:{},促销价格:{},原价:{},生产厂商:{},规格:{},批号:{} '\n'".format(itemName,price,highPrice,factoryName,specification,allowNumber))
        #mysql
        db.ping(reconnect=True)
        sql = 'replace into ypzdw.ypzdwshouye(itemName,price,highPrice,factoryName,specification,allowNumber) values (%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (itemName,price,highPrice,factoryName,specification,allowNumber))
            db.commit()
        except:
            db.rollback()
        db.close()


if __name__ == '__main__':
    cbhhurl = 'https://card.ypzdw.com/card/get?callback=jQuery111309332705544967648_1557210605354&id=product&card_productIds=563657%2C20226%2C104307%2C9174%2C7533%2C384433%2C20863%2C19079%2C16829%2C41762&card_areaCode=510104&entries=basic%2Cprice%2Cpic&pageIndex=1&pageSize=10&_=1557210605366'
    # djrxurl = 'https://card.ypzdw.com/card/get?callback=jQuery111304102465439509051_1557217544831&id=product&card_productIds=17958%2C19216%2C398167%2C181%2C376252&card_areaCode=510104&entries=basic%2Cprice%2Cpic&pageIndex=1&pageSize=10&_=1557217544844'
ypzdw_shouye_cbhh()








