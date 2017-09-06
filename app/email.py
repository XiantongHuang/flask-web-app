# -*- coding: utf-8 -*-

from . import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread


#synchronous emails
def send_asyn_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kw):
    app = current_app._get_current_object()#获取当前运行的程序实例；因为开了新线程，所以不能用current_app()直接获取
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_asyn_email, args=[app, msg])
    thr.start()
    return thr

