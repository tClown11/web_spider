from datetime import datetime
from time import time

import jwt

from flask_microblog.app import login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_microblog.app import db

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


#Flask_Login用户加载功能
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now)


    '''
    User'是关系的右侧实体（左侧实体是父类）。由于这是一种自我指涉关系，我必须在两边使用相同的类。
    secondary 配置用于此关系的关联表，我在此类之上定义了该关联表。
    primaryjoin表示将左侧实体（跟随者用户）与关联表链接的条件。关系左侧的连接条件是follower_id与关联表的字段匹配的用户ID 。所述followers.c.follower_id表达引用follower_id的关联表的列中。
    secondaryjoin表示将右侧实体（跟随的用户）与关联表链接的条件。这个条件与for的类似primaryjoin，唯一不同的是现在我正在使用followed_id，这是关联表中的另一个外键。
    backref定义如何从右侧实体访问此关系。从左侧开始，关系被命名followed，因此从右侧我将使用该名称followers来表示链接到右侧目标用户的所有左侧用户。附加lazy参数表示此查询的执行模式。一种模式，dynamic将查询设置为在特定请求之前不运行，这也是我如何设置帖子的一对多关系。
    lazy类似于同名参数backref，但这一个适用于左侧查询而不是右侧。
    '''
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )




    def __repr__(self):
        return '<User {}'.format(self.username)


    #密码加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    #密码验证
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def  avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
        )


    '''添加和删除关注者'''
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0




    '''关注帖子查询'''
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


    '''重置密码令牌方法'''
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Post {}>'.format(self.body)

