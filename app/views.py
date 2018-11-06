from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
from flask import session
from app.models import Login
from app import app, db
import pandas as pd

app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

@app.route('/')
@app.route('/index')
def index():
	return render_template('login.html')

def CreateMessFile(messFileName):
	open('app/UserFiles/'+messFileName, "wb").close()
	# datelist = pd.date_range(end=pd.datetime.today().date(), periods=180).tolist()
	# l = [0] * 16
	# for i in range(181):
	# 	newDateEntry={'date':datelist[i],'mess_meal':l,'total':0}
	# 	with open("UserFiles/"+messFileName, "ab") as f:
	# 		pickle.dump(newDateEntry,f)

@app.route('/cancel')
def cancel():
	return render_template('cancel.html')


@app.route('/register')
def register():
	return render_template('login.html')

@app.route('/registerNext', methods = ['GET','POST'])
def registerNext():
	messFileName=request.form["email"]+".txt"
	user = Login(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"], password=request.form['loginpassword'], messFile=messFileName)
	db.session.add(user)
	db.session.commit()

	CreateMessFile(messFileName)
	flash('Your account has been created! You are now able to log in', 'success')
	return "Register Successful for: %s" % user.firstname


@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/loginNext',methods=['GET','POST'])
def loginNext():

	if request.method == "POST":
		email = request.form['Lemail']
		password = request.form['Lloginpassword']
		# Can perform some password validation here!
		user  = Login.query.filter(and_(Login.email == email, Login.password == password)).first()
		if user:
			flash('Login successful', 'success')
			return "Login Successful for: %s" % user.firstname
		return "Password Error"

@app.route('/home.html')
@app.route('/home')
def home():
	return render_template('home.html')
