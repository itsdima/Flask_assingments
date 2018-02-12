from flask import Flask, render_template, request, redirect, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
	if len(request.form['firstname']) < 1 or len(request.form['DOB']) < 1 or len(request.form['lastname']) < 1 or len(request.form['email']) < 1 or len(request.form['password']) < 1 or len(request.form['confirm']) < 1:
		flash(u'Please fill all required fields!', 'alert')
		return redirect('/')
	if request.form['password'] != request.form['confirm']:
		flash('Passwords did not match!')
		return redirect('/')
	if len(request.form['password']) < 8:
		flash('Weak password, try 8 or more characters!')
		return redirect('/')
	numcount = 0
	for y in request.form['password']:
		if y.isdigit():
			numcount = 1
	if numcount < 1:
		flash("Your password must contain at least 1 number!")
		return redirect('/')
	temp = request.form['password'].lower()
	if request.form['password'] == temp:
		flash("Your password should contain at least one upper case letter")
		return redirect('/')
	for i in request.form['firstname']:
		if i.isdigit():
			flash('Your name cannot contain any numbers!')
			return redirect('/')
	for x in request.form['lastname']:
		if x.isdigit():
			flash('Your name cannot contain any numbers!')
			return redirect('/')
	if not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid Email Adress!')
		return redirect('/')
	else:
		flash('Registration complete! Please check your email for further instructions')
	return redirect('/')
app.run(debug=True)