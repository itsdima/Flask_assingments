from flask import Flask, redirect, render_template, session, request
import random
import time

app = Flask(__name__)
app.secret_key = 'secret'
app.static_folder = 'static'

@app.route('/')
def home(): 
	if 'totalgold' not in session:
		session['totalgold'] = 0
	if 'log' not in session:
		session['log'] = ''
	return render_template('index.html', totalgold=session['totalgold'], log=session['log'])

@app.route('/process_money', methods=['POST'])
def process():
	if request.form['action'] == 'farm':
		num = random.randrange(10, 20)
		session['totalgold'] += num
		session['log'] += "You Earned "+str(num) +  " golds from Farm! \n"
		print session['log']
	if request.form['action'] == 'cave':
		num = random.randrange(5, 10)
		session['totalgold'] += num
		session['log'] += "You Earned "+str(num)+ " golds from Cave! \n"  #(time.strftime("%I:%M:%S"))
		print session['log']
		print num
	if request.form['action'] == 'house':
		num = random.randrange(2, 5)
		session['totalgold'] += num
		session['log'] += "You Earned "+str(num)+ " golds from House! \n"
		print session['log']
	if request.form['action'] == 'casino':
		num = random.randrange(-50, 50)
		session['totalgold'] += num
		if num > 0:
			session['log'] += "You entered casino and earned "+str(num)+ " golds! NICE! \n"
		else:
			session['log'] += "You entered casino and lost "+str(num)+ " golds... OUCH! \n"
		print session['log']
		print num
	return redirect('/')
app.run(debug=True)