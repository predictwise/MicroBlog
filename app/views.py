__author__ = 'zcq'
#coding:utf-8

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm, PostForm, SearchForm
#第一个app是app文件夹, 第二个app是__init__.py中创建的Flask()对象
from app import app, db, lm, oid
from .models import User, Post
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
#from emails import follower_notification

#从数据库加载用户
@lm.user_loader
def load_user(id):
    print 'load_user:'+str(User.query.get(int(id)))
    return User.query.get(int(id))


#添加登录的用户到全局变量 flask.g.user 中
#在数据库中更新用户最后一次的访问时间
@app.before_request
def before_request():
    print current_user
    #全局变量 current_user 是由 Flask-Login 提供的, 获取当前的登录用户
    #g保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别
    g.user = current_user

    print 'g.user: ', g.user

    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()
        #创建一个搜索表单对象search_form,让他在所有模板中可用,并放入全局变量g中
        #g保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别
        g.search_form = SearchForm()

    return


#显示主页
#从"/"和"/index"网址上都能访问到显示"hello,chaoquan"的这个网页
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    print "hello,i'm index"

    #提交一条新的微博内容(post)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.now(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    '''
    if post_id != 0:
        print 'current page: ', page
        #cur_page = page
        #print 'post_id: ', post_id
        del_post = Post.query.filter_by(id=post_id).first()
        print 'post delete: ', del_post
        db.session.delete(del_post)
        db.session.commit()
        return redirect(url_for('index', page))
    '''
    # 返回Paginate对象, 即pagina是一个Paginate对象,
    # 其中包含这些成员变量: has_next, has_prev, next_num, prev_num
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    # 但目前posts只是Paginate对象,需要用posts.items来解析获取其中的id,timestamp等属性
    return render_template('index.html', title='Home', form=form, posts=posts)


#删除一条微博记录
@app.route('/index/<int:current_page>/del/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(current_page, post_id):
    print 'current page: ', current_page
    #print 'post_id: ', post_id
    del_post = Post.query.filter_by(id=post_id).first()
    print 'post delete: ', del_post
    db.session.delete(del_post)
    db.session.commit()
    return redirect(url_for('index'))



#修改个人简介信息
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    #form = EditForm(g.user.nickname)
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
#oid.loginhandle 告诉 Flask-OpenID 这是我们的登录视图函数
@oid.loginhandler
def login():
    if g.user is None:
        print 'user is none'
    else:
        print 'user is not none'

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm() #实例化一个对象form,不通过new
    #当表单正在展示给用户的时候调用它，它会返回 False.
    if form.validate_on_submit():
        print form.remember_me.data
        session['remember_me'] = form.remember_me.data #这是一个布尔值
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
#resp包含了OpenID提供商返回来的信息
def after_login(resp):
    #判断登录的邮箱是否正确
    if resp.email is None or resp.email == "":
        flash('Invalid login.Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.splite('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        #让用户自己关注自己
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    #记住登录状态,即记住账号和密码
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    # 返回Paginate对象, 即posts是一个Paginate对象,
    # 其中包含这些成员变量: has_next, has_prev, next_num, prev_num
    # 但目前posts只是Paginate对象,需要用posts.items来解析获取其中的body,timestamp等属性
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', user=user, posts=posts)

#关注其他的用户(还未实现)
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow '+nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following '+nickname)
    #follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


#取消关注某一用户(还未实现)
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot follow '+nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following '+nickname)
    return redirect(url_for('user', nickname=nickname))


#全文搜索
@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    #url_for()的第一个参数是一个函数名, 这里代表下面的search_results()函数
    #第二个参数query, 是传入search_results()函数中的参数
    return redirect(url_for('search_results', query=g.search_form.search.data))


#显示全文搜索的结果
@app.route('/search_results/<query>')
@login_required
#参数query的值, 接受自上面的redirect()中的query
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)


