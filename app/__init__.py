# -*- coding: utf-8 -*-

'程序包的构造文件'

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

#尚未初始化所需的实例，创建扩展类时先不传入参数
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

#定义工厂函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])#导入配置
    #config[config_name]从字典取值出来一个类, 类有个静态方法init_app, 这个方法什么也没有做, 是为了方便扩展。
    config[config_name].init_app(app)
    
    #利用扩展自身提供的初始化方法：init_app(),加载响应配置
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
        
    #注册蓝本;路由和自定义错误界面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
