from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re, md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'wall')
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
	return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
	query = 'select * from users'
	users = mysql.query_db(query)
	registered = False
	for i in range(0, len(users)):
		if request.form['logemail'] == users[i]['email'] and md5.new(request.form['logpassword']).hexdigest() == users[i]['password']:
			registered = True
			session['active_user'] = users[i]['id']
			return redirect('/wall')
		else:
			flash('Incorrect Email/Password, Try Again')
			return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect('/')

@app.route('/wall')#, methods=['GET'])
def wall():
	if 'active_user' not in session:
		return redirect('/')
	query = 'select * from users where users.id = {}'.format(session['active_user'])
	users = mysql.query_db(query)
	posts = 'SELECT posts.id, post, posts.created_at, concat(first_name," ",last_name) AS name FROM posts JOIN users ON users.id = posts.users_id GROUP BY posts.created_at desc'
	post = mysql.query_db(posts)
	comments = 'SELECT posts_id, comment, comments.created_at, concat(first_name," ",last_name) AS name FROM comments JOIN users ON users.id = comments.users_id'
	comment = mysql.query_db(comments)
	return render_template('wall.html', all_comments=comment, all_posts=post, all_users=users, active_user=session['active_user'], users=users)

@app.route('/processpost', methods=['POST'])
def post():
	query = "insert into posts (post, created_at, updated_at, users_id) values (:post, now(), now(), :users_id)"
	data = {
			'post': request.form['mypost'],
			'users_id': session['active_user']
			}
	mysql.query_db(query, data)
	return redirect('/wall')

@app.route('/processcomment', methods=['POST'])
def comment():
	query = "insert into comments (comment, created_at, updated_at, users_id, posts_id) values (:comment, now(), now(), :users_id, :posts_id)"
	data = {
			'comment': request.form['mycomment'],
			'users_id': session['active_user'],
			'posts_id': request.form['postid']
			}
	mysql.query_db(query, data)
	return redirect('/wall')

app.run(debug=True)