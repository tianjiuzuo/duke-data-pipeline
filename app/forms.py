from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


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
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CollectionForm(FlaskForm):
    organization = SelectField(
        'Organization',
        choices = [('dcrc', 'Durham Crisis Response Center'), ('nccadv-d', 'North Carolina Coalition Against Domestic Violence - Durham')]
    )
    number_of_victims = IntegerField('Number of victims currently housed', validators=[DataRequired()])
    capacity = IntegerField('What is the planned capacity of the shelter?', validators=[DataRequired()])
    verification = BooleanField('I verify that this information is accurate to the best of my knowledge', validators=[DataRequired()])
    submit = SubmitField('Submit')
