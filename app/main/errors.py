# -*- coding:utf-8 -*-

from flask import render_template
from . import main

#errorhandler只有蓝本中的错误才能触发，使用app_errorhandler可以全局
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

