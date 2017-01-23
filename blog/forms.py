from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.fields import PasswordField
from wtforms.fields import BooleanField
from wtforms.fields import SubmitField
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, ValidationError
from blog.models import Admin


class LoginForm(Form):
    adminname = StringField('AdminID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(Form):
    adminname = StringField('adminname', validators=[DataRequired(),
                            Length(3, 80), Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Usernames consist of numbers, letters,\
                            and underscores.')])
    password = PasswordField('password', validators=[DataRequired(),
                            EqualTo('password2',
                            message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_username(self, username_field):
        if Admin.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class AddForm(Form):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    tag = StringField('tag')


class ModifyForm(Form):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    tag = StringField('tag', validators=[DataRequired()])