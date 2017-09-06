#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


#为shell命令添加一个上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)#注册程序，数据库实例及模型
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

#启动单元测试的命令；修饰器自定义命令，修饰函数名就是命令名
@manager.command
def test():
    """Run the unit tests."""#文档字符串会显示在帮助消息中
    import unittest
    #TestLoader()类的dicover()方法自动在'test'目录下匹配'test_*.py'，并将查找到的测试用实例组装到测试套件，可以用run()直接执行
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
