#!usr/bin/env python
# -*- coding: utf-8 -*-

'a little flasky web app'

__author__ = 'xthuang'


from flask import Flask
from flask_script import Manager#输出一个Manager类，使支持命令行选项。


app = Flask(__name__)#创建程序实例
manager = Manager(app)#把程序实例作为参数传给构造函数，初始化主类的实例。

@app.route('/')#注册视图函数 根目录
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
