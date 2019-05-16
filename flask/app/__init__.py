from flask import Flask
#导入配置文件
from config import Config
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了
#添加配置信息
app.config.from_object(Config)
from app import routes