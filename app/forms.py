from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)], render_kw={'class': 'form-control form-control-lg'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control form-control-lg'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={'class': 'form-control form-control-lg'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)], render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary btn-lg w-100'})

    def validate_confirm_password(self, field):
        if self.password.data != field.data:
            raise ValidationError('Passwords must match.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'class': 'form-control form-control-lg'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary btn-lg w-100'})


class SeminarForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'class': 'form-control'})
    topic = StringField('Topic', validators=[DataRequired()], render_kw={'class': 'form-control'})
    speaker = StringField('Speaker', validators=[DataRequired()], render_kw={'class': 'form-control'})
    hours = DecimalField('Hours', validators=[DataRequired()], places=1, render_kw={'class': 'form-control'})
    organizer = StringField('Organizer', validators=[DataRequired()], render_kw={'class': 'form-control'})
    notes = TextAreaField('Notes', validators=[Optional()], render_kw={'class': 'form-control', 'rows': 4})
    submit = SubmitField('Save Seminar', render_kw={'class': 'btn btn-primary px-4'})
