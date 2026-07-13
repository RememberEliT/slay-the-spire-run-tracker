from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, HiddenField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Email, EqualTo, Optional

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
        coerce=str,
        validators=[
            DataRequired(message="Please choose a character.")
        ]
    )

    floor_reached = IntegerField(
        'Floor reached',
        validators=[
            DataRequired(message="Please enter the floor reached."),
            NumberRange(
                min=1,
                max=57,
                message="Floor reached must be between 1 and 57."
            )
        ]
    )

    ascension_level = IntegerField(
        'Ascension Level',
        validators=[
            DataRequired(message="Please enter the ascension level."),
            NumberRange(
                min=0,
                max=20,
                message="Ascension level must be between 0 and 20."
            )
        ]
    )

    win = BooleanField('Successful run?')

    notes = StringField(
        'Notes',
        validators=[Optional()]
    )

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
