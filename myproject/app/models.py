#coding=utf-8
from werkzeug.security import generate_password_hash,check_password_hash
from __init__ import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
import hashlib
from flask import request

#权限常量
class Permission:
    FOLLOW=0x01
    COMMENT=0x02
    WEITE_ARTICLES=0x04
    MODERATE_COMMENT=0x08
    ADMINISTER=0x80
#创建角色模型或者说角色表
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    #建立关系表
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'% self.name
#在数据库中创建角色
@staticmethod
def inset_roles():
    roles={
        'User':(Permission.FOLLOW|
                Permission.COMMENT|
                Permission.WRITE_ARTICLES,True),
        'Moderator':(Permission.FOLLOW|
                     Permission.COMMENT|
                     Permission.MODERATE_COMMNETS,False),
        'Administrator':(0xff,False)
        }
    for r in roles:
        role=Role.query.filter_by(name=r).first()
        if role is None:
            role=Role(name=r)
        role.permissions=role[r][0]
        role.default=roles[r][1]
        db.session.add(role)
    db.session.commit()
    
#创建用户模型，在数据库中建立表
class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    #建立关系表
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed=db.Column(db.Boolean,default=False)
    #跟goal建立关联
    goals=db.relationship('Goal',backref='user',lazy='dynamic')
    #用户信息字段 
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.Datetime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow())
    #增加用户头像数据
    avatar_hash=db.Column(db.String(32))

    def __repr__(self):
        return '<User %r>'%self.username
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        #初始化使用缓存的MD5散列值生成Gravatar URL
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True
    #刷新用户的最后访问时间
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
        
    #定义默认的用户角色
    if self.role is None:
        if self.email==current_app.config['FLASKY_ADMIN']:
            self.role=Role.query.filter_by(permissions=0xff).first()
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first()
    #检查用户是否有指定权限
    def can(self,permissions):
        return self.role is not None and\
               (self.role.permission & permissions)==permissions
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    #生成用户头像
    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url='http://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url,hash=hash,size=size,default=default,rating=rating)
    def change_email(self,token):
        self.email=new_email
        self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True
    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url='http://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash=self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)
        
    
#建立匿名用户模型
class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False
login_manager.anonymous_user=AnonymousUser

class Goal(db.Model):
    __tablename__=='goals'
    id=db.Column(db.Integer,primary_key=True)
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    create_time=db.Column(db.Dtaetime,index=True,default=datetime.utcnow)
    category=db.Column(db.String(64))
    tile=db.Column(db.String(64))
    plans=db.Column(db.Text)
    completion=db.Column(db.Boolean)

class Category(db.Model):
    __tablename__='category'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    @staticmethod
    def inser_categorys():
        categorys=['study','work','exercise')
        for c in categorys:
            category=Category.query.filter_by(name=c).first()
            if not category:
                category=Category(name=c)
            db.session.add(category)
        db.session.commit()
        
class Plan(db.Model):
    __tablename__='plans'
    id=db.Column(db.Integer,primary_key=True)
    step=db.Column(db.String(64))
    completion=db.Column(db.Boolean)

    






















    
