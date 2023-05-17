from flask_wtf import FlaskForm
from wtforms import DateField, StringField,  PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Optional, EqualTo, ValidationError, Email
from datetime import date

from wtforms.widgets import TextArea

from models import User


class LoginForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj')
    submit = SubmitField('Zaloguj')


class AddTask(FlaskForm):
    title = StringField('Nazwa', validators=[DataRequired(), ])
    description = StringField('Opis', validators=[DataRequired(), ], widget=TextArea())
    creator = StringField('Utworzył', validators=[DataRequired(), ], render_kw={'disabled': 'True'})
    contractor = SelectField('Wykonawca')
    timestamp_created = DateField('Utworzone', default=date.today(), render_kw={'disabled': 'True'})
    timestamp_finished = DateField('Zakończono', validators=[Optional()])
    timestamp_deadline = DateField('Termin', validators=[DataRequired(), ])
    submit = SubmitField('Dodaj')


class EditTask(FlaskForm):
    title = StringField('Nazwa')
    description = StringField('Opis', widget=TextArea())
    creator = StringField('Utworzył', render_kw={'disabled': 'True'})
    contractor = SelectField('Wykonawca')
    timestamp_created = DateField('Utworzone', default=date.today(), render_kw={'disabled': 'True'})
    timestamp_finished = DateField('Zakończono', validators=[Optional()])
    timestamp_deadline = DateField('Termin', validators=[DataRequired(), ])
    submit = SubmitField('Zapisz')


class TaskButtons(FlaskForm):
    delete = SubmitField('Skasuj')
    finish = SubmitField('Zakończ')
    edit = SubmitField('Edytuj')
    comment = SubmitField('Komentarze')


class AddComment(FlaskForm):
    text = StringField('Opis', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Dodaj')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Nazwa użytkownika niedostępna.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Nieprawidłowy adres e-mail.')