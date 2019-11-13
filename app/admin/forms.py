from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class UserTaskForm(FlaskForm):
    article = SelectField('Article', choices=[], coerce=int)
    submit = SubmitField('Add Task from Article')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change password')
