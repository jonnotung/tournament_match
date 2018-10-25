from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tournymatch.models import User, Tournament
from datetime import datetime

class RegistrationForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired(), Length(min = 2, max = 20)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()

		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()

		if email:
			raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
	username = StringField('User Name', validators = [DataRequired()])
	#email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class CreateTournamentForm(FlaskForm):
	name = StringField('Name', validators = [DataRequired()])
	date_scheduled = DateField('Date', format='%Y-%m-%d')
	submit = SubmitField('Create Event')

	def validate_name(self, name):
		name = Tournament.query.filter_by(name = name.data).first()

		if name:
			raise ValidationError('That name for an event is already taken. Please choose another.')

	#def validate_date_scheduled(self, date_scheduled):
	#	now = datetime.today()
	#	if date_scheduled.data() < now.strftime('%Y-%m-%d'):
	#		raise ValidationError('Scheduled date must be in the future.')
		#date = Tournament.query.filter_by(name.like(name.data), date_scheduled.like(date.data) ).first()