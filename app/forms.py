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
    role = SelectField('Role', choices=[('admin', 'admin'), ('shelter', 'shelter'), ('policymaker', 'policymaker')], validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    county = SelectField('County', choices=[('',''),('N/A', 'N/A'),('Alamance', 'Alamance'), ('Alleghany', 'Alleghany'), ('Bladen', 'Bladen'), ('Buncombe', 'Buncombe'), ('Caldwell', 'Caldwell'), 
                                            ('Dare', 'Dare'), ('Davidson', 'Davidson'), ('Forsyth', 'Forsyth'), ('Guilford', 'Guilford'), ('Hertford', 'Hertford'), 
                                            ('Martin', 'Martin'), ('Nash', 'Nash'), ('Pender', 'Pender'), ('Randolph', 'Randolph'), ('Scotland', 'Scotland'), 
                                            ('Stanly', 'Stanly'), ('Vance', 'Vance'), ('Wayne', 'Wayne'), ('Yadkin', 'Yadkin'), ('Wilkes', 'Wilkes'), ('Wilson', 'Wilson'), 
                                            ('Yancey', 'Yancey'), ('Avery', 'Avery'), ('Beaufort', 'Beaufort'), ('Brunswick', 'Brunswick'), ('Cabarrus', 'Cabarrus'), 
                                            ('Catawba', 'Catawba'), ('Chatham', 'Chatham'), ('Cherokee', 'Cherokee'), ('Chowan', 'Chowan'), ('Columbus', 'Columbus'), 
                                            ('Davie', 'Davie'), ('Duplin', 'Duplin'), ('Edgecombe', 'Edgecombe'), ('Franklin', 'Franklin'), ('Gaston', 'Gaston'), ('Graham', 'Graham'), 
                                            ('Granville', 'Granville'), ('Halifax', 'Halifax'), ('Haywood', 'Haywood'), ('Hyde', 'Hyde'), ('Jackson', 'Jackson'), ('Lee', 'Lee'), 
                                            ('McDowell', 'McDowell'), ('Madison', 'Madison'), ('Mitchell', 'Mitchell'), ('New Hanover', 'New Hanover'), ('Orange', 'Orange'), 
                                            ('Pasquotank', 'Pasquotank'), ('Perquimans', 'Perquimans'), ('Pitt', 'Pitt'), ('Richmond', 'Richmond'), ('Rowan', 'Rowan'), 
                                            ('Sampson', 'Sampson'), ('Stokes', 'Stokes'), ('Transylvania', 'Transylvania'), ('Wake', 'Wake'), ('Washington', 'Washington'), 
                                            ('Alexander', 'Alexander'), ('Anson', 'Anson'), ('Ashe', 'Ashe'), ('Caswell', 'Caswell'), ('Cleveland', 'Cleveland'), ('Durham', 'Durham'), 
                                            ('Gates', 'Gates'), ('Harnett', 'Harnett'), ('Iredell', 'Iredell'), ('Lincoln', 'Lincoln'), ('Montgomery', 'Montgomery'), ('Person', 'Person'), 
                                            ('Rockingham', 'Rockingham'), ('Swain', 'Swain'), ('Union', 'Union'), ('Currituck', 'Currituck'), ('Greene', 'Greene'), ('Henderson', 'Henderson'), 
                                            ('Bertie', 'Bertie'), ('Burke', 'Burke'), ('Camden', 'Camden'), ('Carteret', 'Carteret'), ('Johnston', 'Johnston'), ('Lenoir', 'Lenoir'), 
                                            ('Macon', 'Macon'), ('Mecklenburg', 'Mecklenburg'), ('Moore', 'Moore'), ('Watauga', 'Watauga'), ('Surry', 'Surry'), ('Tyrrell', 'Tyrrell'), 
                                            ('Craven', 'Craven'), ('Cumberland', 'Cumberland'), ('Northampton', 'Northampton'), ('Pamlico', 'Pamlico'), ('Polk', 'Polk'), ('Robeson', 'Robeson'), 
                                            ('Clay', 'Clay'), ('Warren', 'Warren'), ('Hoke', 'Hoke'), ('Rutherford', 'Rutherford'), ('Onslow', 'Onslow'), ('Jones', 'Jones')] 
                                            , validators=[DataRequired()])
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
