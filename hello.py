#!usr/bin/env python
# -*- coding: utf-8 -*-

'a little flasky web app'

__author__ = 'xthuang'


from flask import Flask, render_template
from flask_script import Manager#输出一个Manager类，使支持命令行选项。
from flask_bootstrap import Bootstrap#初始化后可以在程序中使用一个包含所有BOOTstrap文件的基模板
from flask_moment import Moment
from datetime import datetime
#定义表单类
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)#创建程序实例
app.config['SECRET_KEY'] = 'SECRET STRING'#设置通用秘钥；Flask-WTF使用这个秘钥生成加密令牌，再用令牌验证请求中表单数据的真伪，防止跨站请求伪造的攻击

#把程序实例作为参数传给构造函数，初始化主类的实例。
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

#web表单，包含一个文本字段和提交按钮；表单中的字段都定义为类变量，类变量值是相应字段类型的对象
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
#像常规路由一样，定义基于模板的自定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#注册视图函数
#index函数不仅要渲染表单，还要接收表单中的数据 v4.0
@app.route('/', methods=['GET', 'POST'])#将表单提交作为POST请求进行处理
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)#current_time变量获取当前utc时间
    #render_templates函数把jinjia2模板集成到程序中，第一个参数是模板的文件名随后     的参数都是键值对（默认在templates文件夹中寻找模板）

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    #左边的name表示参数名，就是模板中的占位符；右边的name是当前作用域中的变量，      表示同名参数值


if __name__ == '__main__':
    manager.run()
