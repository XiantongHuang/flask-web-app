#!usr/bin/env python
# -*- coding: utf-8 -*-

'a little flasky web app'

__author__ = 'xthuang'


from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
