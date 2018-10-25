from datetime import datetime
from tournymatch import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from tournymatch import login

user_tournament_assoc = db.Table('user_tournament_assoc', db.metadata,	
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'))
)

class User(UserMixin, db.Model):
	_tablename_ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(60), nullable=False)
	tournaments = db.relationship('Tournament', secondary=user_tournament_assoc, primaryjoin=(user_tournament_assoc.c.user_id == id), back_populates='users', lazy='dynamic')
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return 'User:{} email:{}'.format(self.username, self.email)

class Tournament(UserMixin, db.Model):
	_tablename_ = 'tournament'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique = True, nullable = False)
	date_scheduled = db.Column(db.Date, nullable = False, default=datetime.today)
	description = db.Column(db.Text, nullable=True)
	users = db.relationship('User', secondary=user_tournament_assoc, primaryjoin=(user_tournament_assoc.c.tournament_id == id), back_populates='tournaments', lazy='dynamic')

	def __repr__(self):
		return 'tournament:{} date:'.format(self.name, self.date_scheduled)

	def is_already_joined(self, user):
		return self.users.filter(user_tournament_assoc.c.user_id == user.id).count() > 0

	def user_joins(self, user):
		if not self.is_already_joined(user):
			self.users.append(user)

	def joined_users(self):
		return self.users

@login.user_loader
def load_user(id):
	return User.query.get(int(id))





	