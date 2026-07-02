from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, HiddenField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Email, EqualTo

from app.models import User
from app import db
import sqlalchemy as sa

class RunForm(FlaskForm):
    character = SelectField(
        label='Character',
        choices=[
            ('ironclad', 'Ironclad'),
            ('silent', 'Silent'),
            ('defect', 'Defect'),
            ('regent', 'Regent'),
            ('necrobinder', 'Necrobinder')
        ],
        coerce=str, validators=[DataRequired()]
    )
    floor_reached = IntegerField('Floor reached',validators=[NumberRange(min=1, max=50),DataRequired()])
    ascension_level = IntegerField('Ascension Level', validators=[NumberRange(min=0, max=10), DataRequired()])
    win = BooleanField('Successful run?')
    notes = StringField('notes')
    submit = SubmitField("Submit")


class ActionForm(FlaskForm):
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
