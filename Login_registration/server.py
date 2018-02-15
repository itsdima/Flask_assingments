from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re, md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'login/registration')
app.secret_key = 'secret'

@app.route('/')
def index():
	query = 'select * from users'
	users = mysql.query_db(query)
	return render_template('index.html', all_users=users)

@app.route('/process', methods=['POST'])
def create():
	runquery = "insert into users (first_name, last_name, email, password, created_at, updated_at) values (:first_name, :last_name, :email, :password, now(), now())"
	rundata = {
			'first_name': request.form['first'],
			'last_name': request.form['last'],
			'email': request.form['email'],
			'password': md5.new(request.form['password']).hexdigest()
			}
	query = 'select * from users'
	users = mysql.query_db(query)
	for i in range(0, len(users)):
		if request.form['email'] == users[i]['email'] or request.form['password'] == users[i]['password']:
			flash('Email/Password is already taken')
			return redirect('/')
	if not EMAIL_REGEX.match(request.form['email']):
		flash('Not a valid Email')
		return redirect('/')
	if len(request.form['first']) < 1 or len(request.form['last']) < 1 or len(request.form['email']) < 1 or len(request.form['password']) < 1 or len(request.form['confirm']) < 1:
		flash('Please fill all required fields!')
		return redirect('/')
	if request.form['password'] != request.form['confirm']:
		flash('Passwords did not match!')
		return redirect('/')
	if len(request.form['password']) < 8:
		flash('Weak password, try 8 or more characters!')
		return redirect('/')
	numcount = 0
	temp = request.form['password'].lower()
	for y in request.form['password']:
		if y.isdigit():
			numcount = 1
	if numcount < 1 or request.form['password'] == temp:
		flash("Your password must contain at least 1 number and 1 upper case letter!")
		return redirect('/')
	for n in request.form['first']:
		if n.isdigit():
			flash('Your name cannot contain any numbers!')
			return redirect('/')
	for x in request.form['last']:
		if x.isdigit():
			flash('Your name cannot contain any numbers!')
			return redirect('/')
	active_user = mysql.query_db(runquery, rundata)
	session['active_user'] = active_user
	print session['active_user']
	return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
	query = 'select * from users'
	users = mysql.query_db(query)
	registered = False
	for i in range(0, len(users)):
		if request.form['logemail'] == users[i]['email'] and md5.new(request.form['logpassword']).hexdigest() == users[i]['password']:
			registered = True
			session['active_user'] = users[i]['id']
			return redirect('/success')
		else:
			flash('Incorrect Email/Password, Try Again')
			return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect('/')

@app.route('/success', methods=['GET'])
def success():
	if 'active_user' not in session:
		return redirect('/')
	query = 'select * from users'
	users = mysql.query_db(query)
	return render_template('success.html', all_users=users, active_user=session['active_user'])

app.run(debug=True)