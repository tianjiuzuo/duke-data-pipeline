from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User, Role


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'admin'), ('shelter', 'shelter')], validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25),
                                                         Regexp("^(?=.*[a-z])", message="Password must have a lowercase character"),
                                                         Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character"),
                                                         Regexp("^(?=.*\\d)", message="Password must contain a number"),
                                                         Regexp("(?=.*[@$!%*#?&])", message="Password must contain a special character")])
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

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=25),
                                                         Regexp("^(?=.*[a-z])", message="Password must have a lowercase character"),
                                                         Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character"),
                                                         Regexp("^(?=.*\\d)", message="Password must contain a number"),
                                                         Regexp("(?=.*[@$!%*#?&])", message="Password must contain a special character")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')

class CollectionForm(FlaskForm):
    number_of_victims = IntegerField('Number of victims currently housed', validators=[DataRequired()])
    capacity = IntegerField('What is the planned capacity of the shelter?', validators=[DataRequired()])
    verification = BooleanField('I verify that this information is accurate to the best of my knowledge', validators=[DataRequired()])
    submit = SubmitField('Submit')
