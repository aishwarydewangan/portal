from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response,flash
from flask import session
from app.models import User, Admin, Menu, Feedback
from app import app, db
from passlib.hash import sha256_crypt
import datetime
import json
from werkzeug import exceptions

app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'


@app.route('/register')
@app.route('/login')
@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
	if 'username' in session:
		return render_template('home.html')
	else:
		return render_template('login.html')


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')

@app.route('/feedbackform', methods=['POST'])
def feedback_form():
	try:
		user = User.query.filter(User.rollNo == session['rollNo']).first()
		feed = Feedback(mess=request.form["mess"],date_of_issue=datetime.datetime.now() , issue=request.form["issue"], description=request.form["description"], user_id=user.id)
		db.session.add(feed)
		db.session.commit()
	except:
		return "Error"
	return "Feedback added successfully"

@app.route('/daywise', methods=['POST'])
def daywise():
	new_day = request.form['day_change']
	new_meal = request.form['time_change']
	print(new_day)
	return render_template('change.html')

def init_json():
	date_list = [datetime.datetime(2019, 6, 30) - datetime.timedelta(days=x) for x in range(540)]
	for item in range(len(date_list)):
		date_list[item] = date_list[item].date()
	dic = {}
	for i in date_list:
		dic[str(i)] = [[[0 for _ in range(4)] for _ in range(4)], 0]
	json_data = json.dumps(dic)
	return json_data


@app.route('/cancel')
def cancel():
	return render_template('cancel.html')


@app.route('/uncancelMeal', methods=['POST'])
def uncancel_meal():
	date_range = request.form['date_range']
	if date_range == '':
		return render_template('error.html')
	try:
		breakfast = request.form['breakfast']
		breakfast = True
	except exceptions.BadRequestKeyError:
		breakfast = False
	try:
		lunch = request.form['lunch']
		lunch = True
	except exceptions.BadRequestKeyError:
		lunch = False
	try:
		dinner = request.form['dinner']
		dinner = True
	except exceptions.BadRequestKeyError:
		dinner = False
	if not (breakfast or lunch or dinner):
		return render_template('error.html')
	else:
		user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
		dic = json.loads(user.json)
		start_date_str, end_date_str = date_range.split(' - ')
		if end_date_str == start_date_str or end_date_str == '...':
			start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
			date_count = 0
		else:
			start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
			end_date = datetime.datetime.strptime(end_date_str, '%d/%m/%Y').date()
			date_count = float((end_date - start_date).days)

		while date_count > -1:
			date = start_date + datetime.timedelta(days=date_count)
			date_str = date.strftime('%Y-%m-%d')
			if breakfast:
				for item in dic[date_str][0][0]:
					if item == -1:
						pos = dic[date_str][0][0].index(item)
						dic[date_str][0][0][pos] = 1
			if lunch:
				for item in dic[date_str][0][1]:
					if item == -1:
						pos = dic[date_str][0][1].index(item)
						dic[date_str][0][1][pos] = 1
			if dinner:
				for item in dic[date_str][0][3]:
					if item == -1:
						pos = dic[date_str][0][3].index(item)
						dic[date_str][0][3][pos] = 1
			date_count -= 1

		json_mod = json.dumps(dic)
		user.json = json_mod
		db.session.commit()

		return redirect(url_for('index'))


@app.route('/cancelMeal', methods=['POST'])
def cancel_meal():
	date_range = request.form['date_range']
	if date_range == '':
		return render_template('error.html')
	try:
		breakfast = request.form['breakfast']
		breakfast = True
	except exceptions.BadRequestKeyError:
		breakfast = False
	try:
		lunch = request.form['lunch']
		lunch = True
	except exceptions.BadRequestKeyError:
		lunch = False
	try:
		dinner = request.form['dinner']
		dinner = True
	except exceptions.BadRequestKeyError:
		dinner = False
	if not (breakfast or lunch or dinner):
		return render_template('error.html')
	else:
		user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
		dic = json.loads(user.json)
		start_date_str, end_date_str = date_range.split(' - ')
		if end_date_str == start_date_str or end_date_str == '...':
			start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
			date_count = 0
		else:
			start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
			end_date = datetime.datetime.strptime(end_date_str, '%d/%m/%Y').date()
			date_count = float((end_date - start_date).days)

		while date_count > -1:
			date = start_date + datetime.timedelta(days=date_count)
			date_str = date.strftime('%Y-%m-%d')
			if breakfast:
				for item in dic[date_str][0][0]:
					if item == 1:
						pos = dic[date_str][0][0].index(item)
						dic[date_str][0][0][pos] = -1
			if lunch:
				for item in dic[date_str][0][1]:
					if item == 1:
						pos = dic[date_str][0][1].index(item)
						dic[date_str][0][1][pos] = -1
			if dinner:
				for item in dic[date_str][0][3]:
					if item == 1:
						pos = dic[date_str][0][3].index(item)
						dic[date_str][0][3][pos] = -1
			date_count -= 1
		json_mod = json.dumps(dic)
		user.json = json_mod
		db.session.commit()

		return redirect(url_for('index'))


@app.route('/view')
def view():
	return render_template('view.html')


@app.route('/change')
def change():
	return render_template('change.html')


@app.route('/changeMeal', methods=['POST'])
def change_meal_date():
	date_range = request.form['date_range']
	if date_range == '':
		return render_template('error.html')
	try:
		breakfast = request.form['breakfast']
		breakfast = True
	except exceptions.BadRequestKeyError:
		breakfast = False
	try:
		lunch = request.form['lunch']
		lunch = True
	except exceptions.BadRequestKeyError:
		lunch = False
	try:
		dinner = request.form['dinner']
		dinner = True
	except exceptions.BadRequestKeyError:
		dinner = False
	mess = request.form['mess']
	if mess == 'North':
		mess_number = 0
	elif mess == 'South':
		mess_number = 1
	elif mess == 'Kadamb':
		mess_number = 2
	elif mess == 'Yuktahar':
		mess_number = 3
	print(mess, mess_number)
	if not (breakfast or lunch or dinner):
		return render_template('error.html')
	user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
	dic = json.loads(user.json)
	start_date_str, end_date_str = date_range.split(' - ')
	if end_date_str == start_date_str or end_date_str == '...':
		start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
		date_count = 0
	else:
		start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
		end_date = datetime.datetime.strptime(end_date_str, '%d/%m/%Y').date()
		date_count = float((end_date - start_date).days)

	while date_count > -1:
		date = start_date + datetime.timedelta(days=date_count)
		date_str = date.strftime('%Y-%m-%d')
		if breakfast:
			for i in range(len(dic[date_str][0][0])):
				dic[date_str][0][0][i] = 0
			dic[date_str][0][0][mess_number] = 1

		if lunch:
			for i in range(len(dic[date_str][0][1])):
				dic[date_str][0][1][i] = 0
			dic[date_str][0][1][mess_number] = 1

		if dinner:
			for i in range(len(dic[date_str][0][3])):
				dic[date_str][0][3][i] = 0
			dic[date_str][0][3][mess_number] = 1
		date_count -= 1

	json_mod = json.dumps(dic)
	user.json = json_mod
	db.session.commit()
	return redirect(url_for('index'))


@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response


@app.route('/admin/register')
@app.route('/admin/login')
@app.route('/admin/index')
@app.route('/admin/')
def adminIndex():
	return render_template('adminLogin.html')


@app.route('/registerNext', methods=['GET', 'POST'])
def registerNext():
	try:
		user = User(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"], rollNo=request.form["rollNo"], password=request.form['loginPassword'], json=init_json())
		db.session.add(user)
		db.session.commit()
	except:
		return "Error: Please check your Email ID or Roll No"
	return redirect(url_for('index'))


@app.route('/admin/registerNext', methods=['GET', 'POST'])
def adminRegisterNext():
	try:
		admin = Admin(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"], mess=request.form["mess"], adminID=request.form["adminID"], password=request.form['loginPassword'])
		db.session.add(admin)
		db.session.commit()
		return "Admin added"
	except:
		return "Error: Please check for following errors: <br />1. Email<br />2.Admin ID"
	return redirect(url_for('dashboard'))


@app.route('/loginNext', methods=['GET', 'POST'])
def loginNext():

	if request.method == "POST":
		rollNo = request.form['rollNo']
		password = request.form['loginPassword']

		user = User.query.filter(User.rollNo == rollNo).first()

		if user:
			session['username'] = user.firstname
			session['rollNo'] = user.rollNo
			session['email'] = user.email
			return redirect(url_for('index'))
		return "Password Error"


@app.route('/admin/loginNext', methods=['GET', 'POST'])
def adminLoginNext():

	if request.method == "POST":
		adminID = request.form['adminID']
		password = request.form['loginPassword']

		admin = Admin.query.filter(Admin.adminID == adminID).first()

		if admin:
			session['username'] = admin.firstname
			session['mess'] = admin.mess
			session['adminID'] = admin.adminID
			session['email'] = admin.email
			return "Login Successful"
		return "Password Error"


@app.route('/admin/change')
def adminChange():
	# time = ["breakfast", "lunch", "snacks", "dinner"]
	# day = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
	# mess = ["north", "south", "yuktahar", "kadamb"]

	# for i in day:
	# 	for j in time:
	# 		for k in mess:
	# 			menu = Menu(mess=k, time=j, day=i, item1="item1", item2="item2", item3="item3", item4="item4", item5="item5", item6="item6", item7="item7", item8="item8", item9="item9", item10="item10", item11="item11", item12="item12")
	# 			db.session.add(menu)
	# 			db.session.commit()

	return render_template('adminChange.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
	if 'username' in session:
		name = session.pop('username')
		email = session.pop('email')
		roll_no = session.pop('rollNo')

	return redirect(url_for('index'))
