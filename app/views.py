from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
from flask import session
from app.models import Login
from app import app, db
import pandas as pd
from passlib.hash import sha256_crypt
import datetime
import json

app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'


@app.route('/index')
@app.route('/')
def index():
	return render_template('login.html')

# def CreateMessFile(messFileName):
# 	open('app/UserFiles/'+messFileName, "wb").close()
	# datelist = pd.date_range(end=pd.datetime.today().date(), periods=180).tolist()
	# l = [0] * 16
	# for i in range(181):
	# 	newDateEntry={'date':datelist[i],'mess_meal':l,'total':0}
	# 	with open("UserFiles/"+messFileName, "ab") as f:
	# 		pickle.dump(newDateEntry,f)


def init_json():
	date_list = [datetime.datetime(2019, 6, 30) - datetime.timedelta(days=x) for x in range(540)]
	for item in range(len(date_list)):
		date_list[item] = date_list[item].date()
	dic = {}
	for i in date_list:
		dic[i] = [[[0 for _ in range(4)] for _ in range(4)], 0]
	json_data = json.dumps(dic)
	return json_data


@app.route('/register')
def register():
	return render_template('login.html')


@app.route('/registerNext', methods=['GET', 'POST'])
def registerNext():
	try:
		# json_name = request.form["rollNo"]
		user = Login(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"], rollNo=request.form["rollNo"], password=request.form['loginpassword'], json=init_json())
		db.session.add(user)
		db.session.commit()
	except:
		return "Email Id or Roll No already exists. Please check again. "
	# CreateMessFile(messFileName)
	flash('Your account has been created! You are now able to log in', 'success')
	return "Register Successful for: %s" % user.firstname


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/loginNext',methods=['GET','POST'])
def loginNext():

	if request.method == "POST":
		rollNo = request.form['LrollNo']
		password = request.form['Lloginpassword']
		
		user = Login.query.filter(and_(Login.rollNo == rollNo, Login.password == password)).first()
		if user:
			flash('Login successful', 'success')
			return "Login Successful for: %s" % user.firstname
		return "Password Error"


@app.route('/home.html')
@app.route('/home')
def home():
	return render_template('home.html')
