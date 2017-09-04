#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
a little flasky web app
'''

__author__ = 'xthuang'

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell#输出一个Manager类，使支持命令行选项;集成Python shell，避免每次启动shell回话都要导入数据库实例和模型
from flask_bootstrap import Bootstrap#初始化后可以在程序中使用一个包含所有BOOTstrap文件的基模板
from flask_moment import Moment
from datetime import datetime
#定义表单类
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
#导入sqlalchemy，使用数据库抽象层/ORM
from flask_sqlalchemy import SQLAlchemy
#使用Flask-Migrate实现数据库迁移
from flask_migrate import Migrate, MigrateCommand
#电子邮件支持
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))#先获取当前目录，再获取当前目录的绝对地址

app = Flask(__name__)#创建程序实例

#app.config字典可用来存储框架、扩展和程序本身的配置变量
#设置通用秘钥；Flask-WTF使用这个秘钥生成加密令牌，再用令牌验证请求中表单数据的真伪，防止跨站请求伪造的攻击
app.config['SECRET_KEY'] = 'SECRET STRING'
#程序使用的数据哭URL必须保存到这个键中
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#设为True 每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#配置Flask-Mail使用qq邮箱发送邮件
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = ['Flasky']
app.config['FLASKY_MAIL_SENDER'] = 'xt_huang@qq.com'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')#接受邮件的邮箱地址

#把程序实例作为参数传给构造函数，初始化主类的实例。
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)#db表示程序使用的数据库，同时获取了Flask-SQLAlchemy提供的所有功能
migrate = Migrate(app, db)
mail = Mail(app)

#web表单，包含一个文本字段和提交按钮；表单中的字段都定义为类变量，类变量值是相应字段类型的对象
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


#定义Role和User模型,从db.Model类继承
class Role(db.Model):
    __tablename__ = 'roles'
    #定义类变量，其为该模型的属性，被定义为db.Column类的实例
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #users属性代表这个关系的面向对象视角;'User'表明关系的另一端是哪个模型；backref参数向User中添加一个role属性，从而定义反向关系。这一属性可以代替role_id访问Role模型，此时获得的是模型对象，而不是外键的值。
    users = db.relationship('User', backref='role', lazy='dynamic')#lazy='dynamic'参数，禁止自动执行查询

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #定义外键，建立起关系；roles 表名
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


#为shell命令添加一个上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)#注册程序，数据库实例及模型

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)#导出数据库迁移命令，使用db命令附加

#发送电子邮件功能
def send_email(to, subject, template, **kw):
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    mail.send(msg) 

#像常规路由一样，定义基于模板的自定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#注册视图函数
@app.route('/', methods=['GET', 'POST'])#将表单提交作为POST请求进行处理
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data =''
        return redirect(url_for('index'))#表单验证成功后执行重定向，跳出index()函数；浏览器收到这种响应，回想重定向的URL发起GET请求，这时表单验证是无法通过的，if 内语句不执行，执行下一条return，利用回话中保存的数据，渲染模板。
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known', False))#current_time变量获取当前utc时间
    #render_templates函数把jinjia2模板集成到程序中，第一个参数是模板的文件名随后的参数都是键值对（默认在templates文件夹中寻找模板）
 
if __name__ == '__main__':
    manager.run()
