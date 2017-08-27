#coding=utf-8
from datetime import datetime
from flask import render_template,session,redirect,url_for
from sys import path
path.append(r'C:\Users\Administrator\myproject')
from __init__ import main
from forms import NameForm
from app import db
from app.models import User


@main.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False),current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)
#资料编辑路由
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been update.')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data=current_user.name
    form.location.data=current_location.data
    form.about_me.data=current_about_me.data
    return render_template('edit_profile.html',form=form)
#管理员的用户资料编辑路由
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/show')
def show():
    goals=Goal.query.filter_by(user_id=current_user.id).all()
    if goals is None:
        flash('你还未曾创建任何目标')
    return render_template('index.html',goals=goals)
@main.route('/add-event',methods=['GET','POST'])
@login_required
def add_goals():
    form=AddGoalForm()
    if form.validate_on_submit():
        goal=Goal(title=form.title.data,
                    category=Category.query.get(form.category.data).name,
                    steps=form.steps.data,
                    user=current_user._get_current_object()
                    )
        db.session.add(goal)
        flash('添加目标成功')
        return redirect(url_for('indext.html')
    return render_template('main/add_goal.html',form=form)

@main.route('/add-category',methods=['GET','POST'])
@login_required
def add_category():
    form=AddCategoryForm()
    if form.validate_on_submit():  
        category=Category(name=form.name.data)
        db.session.add(category)
        flash('类别添加成功')
        return redirect(url_for('indext.html')
     return render_template('main/add_goal.html',form=form)

@main.route('edit-goal/<int:id>',method=['GET','POST'])
@login_required
    def edit_goal(id):
        goal=Goal.query.get_or_404(id)
        form=EditGoalForm()
        if form.validate_on_submit():
            goal.title=form.title.data
            goal.category=Category.query.get(form.category.data).name
            goal.steps=form.steps.data
            db.session.add(event)
            flash('目标已经更新')
        return redirect(url_for('.index'))
    form.title.data=goal.title
    form.category.data=goal.category
    form.steps.data=goal.steps
    return render_template('main/edit_goal.html',form=form)
@main.route('/delete-event/<int:id>',methods=['GET','POST'])
@login_required
def delete_goal(id):
    goal=Goal.query.get_or_404(id)                        
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('.index'))
                        
@main.route('/finish/<int:id>')
@login_required
def finish(id):
    goal=Goal.query.get_or_404(id)
    if step.completion=True
        flash('恭喜你向成功迈进了一步')
    for s in goal.steps:                    
        s.completion=True
        db.session.add(id)
        db.session.commit()
        flash('太棒啦，你已经完成了计划')
        return redirect(url_for('.indext'))
                        





















