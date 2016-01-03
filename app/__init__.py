__author__ = 'zcq'
#coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from flask_mail import Mail


app = Flask(__name__) #创建Flask实例, 让程序知道去哪里找静态文件和模版之类的东西
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
#Flask-OpenID 扩展需要一个存储文件的临时文件夹的路径。对此，我们提供了一个 tmp 文件夹的路径
oid = OpenID(app, os.path.join(basedir, 'tmp'))
mail = Mail(app)

from app import views, models
