import os


class Config(object):
    CSRF_ENABLED = True   #为了激活 跨站点请求伪造 保护
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' #用来建立一个加密的令牌，用于验证一个表单
    POSTS_PER_PAGE = 15


    OPENID_PROVIDERS = [
        { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
        { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
        { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
        { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
        { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    SQLALCHEMY_DATABASE_URI ='mysql+cymysql://root:123456789@127.0.0.1:3306/demo?charset=utf8'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #basedir = os.path.abspath(os.path.dirname(__file__))

    #class Config(object):
        #SQLALCHeMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
           # 'sqlite://' + os.path.join(basedir, 'app.db')
        #SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '785598069@qq.com'
    MAIL_PASSWORD = 'mknqbgukblfpbbfc'
    ADMINS = ['785598069@qq.com']