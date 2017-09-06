# -*- coding: utf-8 -*-

'创建蓝本'

from flask import Blueprint

#通过实例化Blueprint类对象处理蓝本；参数：蓝本的名字，蓝本所在的包或模块
main = Blueprint('main', __name__)

#在末尾导入，避免循环导入依赖
from . import views, errors

