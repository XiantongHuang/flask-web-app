#!usr/bin/env python
# -*- coding: utf-8 -*-

#程序的配置，使用层次结构的配置类，为程序设定多个可能需要的配置


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'YOU KNOW NOTHING'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SENDER = 'xt_huang@qq.com'
    FLAKY_MAIL_SUBJECT_PREFIX = ['Flasky']
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    #定意思init_app方法，在这个方法中执行对当前环境的配置初始化
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


#字典中注册不同的配置环境，注册默认配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodution': ProductionConfig,
    
    'default': DevelopmentConfig
}

    
    
