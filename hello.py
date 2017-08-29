#!usr/bin/env python
# -*- coding: utf-8 -*-

'a little flasky web app'

__author__ = 'xthuang'


from flask import Flask, render_template
from flask_script import Manager#输出一个Manager类，使支持命令行选项。


app = Flask(__name__)#创建程序实例
manager = Manager(app)#把程序实例作为参数传给构造函数，初始化主类的实例。

@app.route('/')#注册视图函数 根目录
def index():
    return render_template('index.html')
    #render_templates函数把jinjia2模板集成到程序中，第一个参数是模板的文件名随后     的参数都是键值对（默认在templates文件夹中寻找模板）

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    #左边的name表示参数名，就是模板中的占位符；右边的name是当前作用域中的变量，      表示同名参数值


if __name__ == '__main__':
    manager.run()
