import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
from jsonpath import jsonpath

# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib
    print(f"user cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookielib
    print(f"user cookielib in python3.")
    import requests
    import re
    from lxml import etree
    from bs4 import BeautifulSoup
    import json
    from jsonpath import jsonpath

# session代表某一次连接
mafengwoSession = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
mafengwoSession.cookies = cookielib.LWPCookieJar(filename = "mafengwoCookies.txt")


userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "http://passport.ypzdw.info/login",
    'User-Agent': userAgent,
}

def mafengwoLogin(account, password):
    # 马蜂窝模仿 登录
    print ("开始模拟终端网")

    postUrl = "http://passport.ypzdw.info/login"
    postData = {
        "username": account,
        "password": password,
    }
    # 使用session直接post请求
    responseRes = mafengwoSession.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
    mafengwoSession.cookies.save()
mafengwoLogin("testcg1", "654321")

# 通过访问个人中心页面的返回状态码来判断是否为登录状态
def isLoginStatus():
    routeUrl = "http://card.ypzdw.info/card/get?callback=jQuery111308877416817205974_1545356568011&id=product&card_productIds=17958%2C99288%2C98095%2C32078%2C183718&card_areaCode=510104&entries=basic%2Cprice%2Cpic&pageIndex=1&pageSize=10&_=1545356568024"
    # 下面有两个关键点
        # 第一个是header，如果不设置，会返回500的错误
        # 第二个是allow_redirects，如果不设置，session访问时，服务器返回302，
        # 然后session会自动重定向到登录页面，获取到登录页面之后，变成200的状态码
        # allow_redirects = False  就是不允许重定向
    responseRes = mafengwoSession.get(routeUrl, headers = header, allow_redirects = False).text
    #print (re.findall(r"\b.lowPrice",responseRes))
    print(responseRes)
    #data = json.loads(responseRes)
    #print(type(data))

    #b = json.loads(a, strict=False)
    #print (b['lowPrice'])

    #json = json.loads(responseRes)
    #ypzdw = mafengwoSession.get(routeUrl).text
    #rint(ypzdw)
    #print(f"isLoginStatus = {responseRes.status_code}")

isLoginStatus()




