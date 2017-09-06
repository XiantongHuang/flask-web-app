# -*- coding: utf-8 -*-

#从当前程序所在目录下的__init__.py导入
from . import db


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

