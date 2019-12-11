from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField, StringField, HiddenField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserTaskForm(FlaskForm):
    article = SelectField('Article', choices=[], coerce=int)
    sentences = MultiCheckboxField('Sentences', coerce=int, choices=[], validators=[])
    submit = SubmitField('Next')


class UserRemoveTasksForm(FlaskForm):
    user_id = HiddenField()
    tasks = MultiCheckboxField('Tasks', coerce=int, choices=[], validators=[])
    submit = SubmitField('Unassign selected tasks')


class ChangePasswordForm(FlaskForm):
    user_id = HiddenField()
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change password')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = PasswordField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditSentenceForm(FlaskForm):
    sentence_id = HiddenField()
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Edit')
