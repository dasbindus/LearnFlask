#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author_ = 'Jack Bai'

import os


class Config:
    '''
    Basic configiration for MYBLOG.
    '''
    SECRET_KEY = 'CaNYoUSeEMeNoW'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MYBLOG_MAIL_SUBJECT_PREFIX = '[MYBLOG INFO]'
    MYBLOG_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    MYBLOG_ADMIN = os.environ.get('MYBLOG_ADMIN')
    MYBLOG_POSTS_PER_PAGE = 20
    MYBLOG_FOLLOWERS_PER_PAGE = 50
    MYBLOG_COMMENTS_PER_PAGE = 15

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    '''
    configiration when developing.
    '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/test_flask'


class TestingConfig(Config):
    '''
    configiration when testing.
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/test_flask'


class ProductionConfig(Config):
    '''
    configiration when producting.
    '''
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/test_flask'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
