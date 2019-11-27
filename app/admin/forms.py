from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired


class UserTaskForm(FlaskForm):
    article = SelectField('Article', choices=[], coerce=int)
    submit = SubmitField('Add Task from Article')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change password')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = PasswordField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
