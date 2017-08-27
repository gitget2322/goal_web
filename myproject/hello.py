#coding=utf-8
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_script import Shell,Manager
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
manager=Manager(app)

#引入数据库
app.config['SQLACHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLACHEMY_COMMIT_ON_TEARDOWN']=True
#下面引入表单
app.config['SECRET_KEY']='hard to guess string'

#下面配置Flask-Mail使用Gmail
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USER_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
   
app.config['FLASKY_ADMIN']=os.environ.get('FLASK_ADMIN')


db=SQLAlchemy(app)
moment=Moment(app)
mail=Mail(app)
@app.route('/',methods=['GET','POST'])
def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        user=User.query.filter_by(username=form.name.data).first()
        if old_name is not None and old_name!=form.name.data:
            flash('Looks like you have changed your name!')
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        return redirect(url_for('index'))
        form.name.data=''
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False),current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',current_time=datetime.utcnow())

if __name__=='__main__':
    app.run()#从app.run(debug=Ture)修改而来（因为加了Flask-Script）加了Manger

#创建角色模型或者说角色表
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    #建立关系表
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'% self.name
#创建用户模型或者说用户表
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    #建立关系表
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'%self.username
bootstrap=Bootstrap(app)#为使首页显示欢迎消息，引入bootstrap建立HTML模板

#定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
#定义表单类
class NameForm(Form):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('Submit')
    
#为shell命令添加一个上下文
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,mail=mail)
manager.add_command("shell",Shell(make_context=make_shell_context))

#异步发送电子邮件
def send_async_email(app,msg):
    with app.app_context():#Flask-Mail中的send（）函数使用current_app，所以必须激活程序上下文
        mail.send(msg)
def send_email(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr=.start()
    return thr


