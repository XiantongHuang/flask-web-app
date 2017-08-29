#!usr/bin/env python
# -*- coding: utf-8 -*-

'a little flasky web app'

__author__ = 'xthuang'


from flask import Flask
app = Flask(__name__)#创建程序实例


@app.route('/')#注册视图函数 根目录
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
