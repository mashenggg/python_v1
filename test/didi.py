import requests
url='https://page.udache.com/driver-biz/driver-recruitment/index.html'

data=requests.get(url).text
print(data)