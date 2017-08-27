# -*- coding: cp936 -*-
from flask_wtf import FlaskForm,Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class LoginForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required()])
    remember_me=BooleanField('Keep me logged in')
    sumbit=SubmitField('Log In')
#���ϱ༭��    
class EditProfileForm(Form):
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Loaction',validators=[Length(0,64)])
    abourt_me=TextAreaField('About me')
    submit=SubmitField('Submit')
#����Աʹ�õ����ϱ༭��
class EditProfileAdminForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                               'Usernames must have only letters.'
                                                                               'numbers,dots or underscores')])
    confirmed=BooleanField('Confirmed')
    role=SelectField('Role',coerce=int)
    name=StringFiedl('Real name',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name)
                           for role in Role.query.order_by(Role.name).all()]
        self.user=user
    def validate_email(self,field):
        if field.data!=self.user.email and\
           User.query.filter_by(email=field.data).first():
         raise ValidationError('Email already registered.')
    def validate_username(self,field):
        if field.data!=self.user.username and\
           User.query.filter_by(username=field.data).first():
          raise ValidationError('Username already in use.')
#���Ŀ���
class AddGoalForm(FlaskForm):
    title=StringField('Ŀ��&����',validators=[Required()])
    category=SelectField('���',coerce=int)
    steps=TextArea('����'):
        class AddStepForm(FlaskForm):
            step=StringField(validators=[Required()])
            submit=SubmitField('���')
        
    
    submit=SubmitField('���')

    def __init__(self,*args,**kwargs):
        super(AddGoalForm,self).__init__(*args,**kwargs)
        self.category.choices=[(category.id,category.name)
                               for category in Category.query.order_by(Category.name).all()]
        
class EditGoalForm(FlaskForm):
    title=StringField('Ŀ��&����',validators=[Required()])
    category=SelectField('���',coerce=int)
    steps=TextArea('����'):
        class EditStepForm(FlaskForm):
            step=StringField(validators=[Required()])
            submit=SubmitField('�޸�')
        
    
    submit=SubmitField('�޸�')
    def __init__(self,*args,**kwargs):
        super(EditGoalForm,self).__init__(*args,**kwargs)
        self.category.choices=[(category.id,category.name)
                               for category in Category.query.order_by(Category.name).all()]

class AddCategoryForm(FlaskForm):
    name=StringField('���',validators=[Required()])
    submit=SubmitField('���')

    def validate_name(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('����Ѿ�����')


    
















