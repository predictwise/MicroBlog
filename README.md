#### 作者：章超权，刘璐
#### Hello guys, this is my first blog with Python2.7, Bootstrap, Flask and sqlite3
#### 1. 克隆
每次克隆之后, 在使用项目之前, 要先激活相应的环境
+ $cd Blogzcq
+ $virtualenv flask
+ $. flask/bin/activate (注意有".")

#### 退出虚拟环境使用如下命令
+ $deactivate

#### 2. 启动
在终端启动, 查看微博网站效果
+ $python run.py

#### 3. 访问
然后在你的浏览器的地址栏中输入http://127.0.0.1:5000/, 即可访问到微博网站的登录页面.在登录页面中, 只需  
从列表中选择你的OpenID(比如Google, Yahoo, Flickr等)即可进行访问, 或者在输入框中自行输入你的OpenID.  
OpenID即为一个公共账号. 比如你有一个google账号, 也就是说你拥有了一个公共账号, 两者是通用的.  
目前我只有Yahoo上有一个OpenID, 登录过程需要等待几秒钟.
+ 账号: chaoquan.zhang@yahoo.com
+ 密码: 12045zcq

与此同时你也可以选择记住账号密码, 以便下次无需任何登录即可访问你的主页. 但是我并不建议这么做.

#### 4. 首页
进入首页你将主要看到三个部分, 最顶部的导航栏部分, 中间的发表微博部分, 以及下方的已发微博列表部分.

#### 5. 导航栏
导航栏一共包含四个功能按钮: "Home", "Your Profile", "Logout", "Search"

#### 5.1 Home
"Home"的功能为返回主页面, 无论你在哪都能一键返回主页面.  

#### 5.2 Your Profile
"Your Profile"的功能为显示你的个人信息, 比如你的昵称, 你的个性签名, 你上次登录的时间戳, 以及你关注  
的人和粉丝数量.你也可以点击"Edit your profile"按钮, 随时更改你的昵称以及个性签名, 别忘了保存就行.

#### 5.3 Logout
"Logout"的功能为安全退出, 返回到登录页面.

#### 5.4 Search
"Search"实现全文搜索的功能, 你只需在搜索框中输入你想要查找的关键字并回车, 即可搜索到你所有已发微博中包  
含这关键字的结果列表

#### 6. 发表微博
只需在"say something"输入框中任意输入你想说的话即可, 可以是一天的心情, 人生感悟等. 一旦博文发表成功之  
后, 会置顶显示.抱歉目前还暂不支持上传图片, 但我会在以后更新这一功能. 

#### 7. 微博列表
此列表中包含了所有你之前发过的微博, 以时间的新旧排序. 每一条博文上都会记载着你发表的时间, 而且点击你的  
头像页面也将会跳转到个人信息页面. 在列表的最下方你会看到"Prev"和"Next", 这是翻页按钮, 点击"Next"会翻到  
下一页, 同理点击"Prev"将会翻到上一页.  
当然也支持删除博文功能, 你只需点击每行列表右侧的红色"delete"按钮即可删除该条微博.

#### 8. 关键的controller层  
关键的业务层代码主要存在于"views.py"中, 下面罗列一些主要的函数:
+ load_user(id)  
id: 为该用户在数据库中存储的编号  
该函数从数据库中加载用户

+ login() 
显示登录页, 让用户进行登录

+ after_login(resp)  
resp: 包含了OpenID提供商返回回来的信息. 比如账号和密码是否正确等.

+ before_request()  
添加登录用户到全局变量"g.user"中, 并创建一个全文搜索的表单对象, 让他在所有模板中可用  
在数据库中更新用户最后一次的访问时间

+ index(page=1)  
page=1: 默认显示微博列表的第一页  
显示主页

+ delete()  
删除一条微博记录

+ edit()  
修改个人简介信息

+ user(nickname, page=1)  
nickname: 为用户的微博昵称  
page=1: 为将显示的用户个人简介置于微博列表第一页中  
显示用户的个人简介

+ follow(nickname)  
nickname: 为要关注的用户对象的昵称  
关注其他用户(还未实现)

+ unfollow(nickname)  
nickname: 为要取消关注的用户对象的昵称  
取消关注某一用户

+ search()
在自己的所有已发的微博中进行全文搜索. 输入关键字, 搜索出包含该关键字的相关微博  
使用了flask_whooshalchemy这一全文搜索引擎

+ search_results(query)
query: 为输入的关键字  
显示全文搜索的结果

+ logout()  
安全退出

#### 9. model层  
数据库的表结构比较简单, 只有user表, post表和followers表, 使用了sqlalchemy进行封装
