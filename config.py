__author__ = 'zcq'
#coding:utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI 是 Flask-SQLAlchemy 扩展需要的。这是我们数据库文件的路径
#当前目录下的app.db数据库
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO 是文件夹，我们将会把 SQLAlchemy-migrate(用来跟踪数据库的更新) 数据文件存储在这里
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#支持Flask的唯一纯python全文搜索引擎Whoosh
WHOOSH_BASE = os.path.join(basedir, 'search.db') #配置

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

#pagination
POSTS_PER_PAGE = 3

#全文搜索最大返回结果数
MAX_SEARCH_RESULTS = 50

#用于发送邮件的email server
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

#admin list
ADMINS = ['nimozcq@163.com']
