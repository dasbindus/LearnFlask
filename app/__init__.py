#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    '''
    create_app() 函数就是程序的工厂函数,接受一个参数,是程序使用的配置名。
    配置类在 config.py 文件中定义,其中保存的配置可以使用 Flask app.config 
    配置对象提供的 from_object() 方法直接导入程序。至于配置对象,则可以通过
    名字从 config 字典中选择。

    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # ============附加路由和自定义的错误页面===========
    # 
    # 在BluePrint中定义的路由处于休眠状态,直到蓝本注册
    # 到程序上后,路由才真正成为程序的一部分
    # 
    # 
    # ===============================================
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth') # 注册后Blueprint中定义的所有路由都会加上指定的前缀, e.g. /login => /auth/login

    return app