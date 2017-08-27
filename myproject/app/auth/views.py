#coding=utf-8
from flask import render_template
from __init__ import auth
from flask_login import logout_user,login_required
from app.email import send_email
from flask_login import current_user


@auth.before_app_request
def before_request():
    if current_user.is_authenticated()\
       and not current_user.confirmed\
       and request.endpoint[:5]!='auth.':
        and request.endpoint!='static':
    return redirect(url_for('auth.unconfirmed'))
#更新已登录用户访问时间
    if current_user.is_authenticated():
        current_user.ping()
        if not current_user.confirmed \
           and required.endpoint[:5]!='auth':
           return redirect(url_for('auth.unconfirmed')
                           
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login')
@login_required
def login():
    return render_template('auth/login.html')

@auth.route('/login')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
#注册用的路由
@auth.route('/register',methods=['GET','POST'])
@def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account',
                   'auth/email/confirm',user=user,token=token)
        
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user..confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('mian.index'))
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm your account',
               'auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))


    
