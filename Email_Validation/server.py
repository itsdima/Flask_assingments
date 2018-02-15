from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'email')
app.secret_key = 'secret'

@app.route('/')
def index():
	if 'check' not in session:
		session['check']= ''
	if 'email' not in session:
		session['email'] = ''
	query = 'select * from email'
	emails = mysql.query_db(query)
	return render_template('index.html', all_emails=emails, check=session['check'])

@app.route('/process', methods=['POST'])
def create():
	runquery = "insert into email (email, created_at, updated_at) values (:email, now(), now())"
	rundata = {
			'email': request.form['email']
			}
	query = 'select * from email'
	emails = mysql.query_db(query)
	for i in range(0, len(emails)):
		if request.form['email'] == emails[i]['email']:
			session['check'] = False
			return redirect('/')
	if not EMAIL_REGEX.match(request.form['email']):
		session['check'] = False
		return redirect('/')
	session['check'] = True
	session['email'] = request.form['email']
	mysql.query_db(runquery, rundata)
	return redirect('/success')

@app.route('/success', methods=['GET'])
def success():
	query = 'select * from email'
	emails = mysql.query_db(query)
	return render_template('success.html', all_emails=emails, check=session['check'])

app.run(debug=True)