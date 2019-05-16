#从app模块中即从__init__.py中导入创建的app应用
from app import app
from flask import render_template
#导入表单处理方法
from app.forms import LoginForm
from flask import render_template,flash,redirect,url_for

#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
@app.route('/')
# @app.route('/test')
def hello():
    return "Hello,World!"
@app.route('/test')
def test():
    user = {'username':'masheng'}

    return render_template('index.html',title='',user=user)
# @app.route('/test1')
# def test1():
#     user = {'username':'duke'}
#     posts = [
#         {
#             'author':{'username':'刘'},
#             'body':'这是模板模块中的循环例子～1'
#
#         },
#         {
#             'author': {'username': '忠强'},
#             'body': '这是模板模块中的循环例子～2'
#         }
#     ]
#     time ="2019"

    # return render_template('index.html', title='', user=user,posts=posts,time=time)
@app.route('/login',methods=['GET','POST'])
def login():
    #创建一个表单实例
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('test'))