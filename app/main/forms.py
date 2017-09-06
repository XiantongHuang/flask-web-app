# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

#web表单，包含一个文本字段和提交按钮；表单中的字段都定义为类变量，类变量值是相应字段类型的对象
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

