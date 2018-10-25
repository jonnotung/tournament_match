from flask import render_template, url_for, flash, redirect, request
from tournymatch import app, db, bcrypt
from tournymatch.models import User, Tournament
from tournymatch.forms import LoginForm, RegistrationForm, CreateTournamentForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/home")
def index():
	events = Tournament.query.all()
	return render_template('home.html', tournys=events)

@app.route("/event/<id>")
def event(id):
	event = Tournament.query.filter_by(id=id).first()
	return render_template('events.html', event=event)

@app.route("/even/<id>/join")
def join_event(id):
	event = Tournament.query.filter_by(id=id).first()
	return render_template('events.html', event=event)

@app.route('/create_event', methods = ['GET', 'POST'])
@login_required
def create_event():
	form = CreateTournamentForm()
	if form.validate_on_submit():
		event = Tournament(name = form.name.data, date_scheduled = form.date_scheduled.data)
		db.session.add(event)
		db.session.commit()
		flash('Event created!', 'success')
		return redirect(url_for('index'))
	return render_template('create_event.html', title = 'Create Event', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('login'))
	
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		flash('Already logged in.', 'success')
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(f'Incorrect user / password combination.', 'danger')
			return redirect(url_for('login'))

		login_user(user, remember=form.remember.data)
		next_page = request.args.get('next')
		flash(f'Login successful.', 'success')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(url_for('create_event'))

	return render_template('login.html', title='Sign In', form=form)

@app.route('/users')
def user_list():
	users = User.query.all()
	return render_template('user_list.html', users=users)

@app.route('/logout')
def logout():
	logout_user()
	flash(f'You have logged out.', 'success')
	return redirect(url_for('index'))



#@app.route("/user/<name>")
#def user(name):
#	return '<h1>Hello {}!</h1>'.format(name)