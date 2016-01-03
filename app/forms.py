__author__ = 'zcq'
#coding:utf-8

from flask_wtf import Form
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    #DataRequired 验证器只是简单地检查相应域提交的数据是否是空
    #validators: 验证器
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    #设置输入域最长的长度为140个字符
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])