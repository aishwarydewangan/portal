from flask import render_template
from sqlalchemy import and_
from flask import url_for, redirect, request, make_response, flash
from flask import session
from app.models import User, Admin, Menu, Feedback, Rates
from app import app, db
from passlib.hash import sha256_crypt
import datetime
from calendar import monthrange
import json
from werkzeug import exceptions

app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'


@app.route('/register')
@app.route('/login')
@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    error = {}
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('login.html', error=error)


# @app.route('/download')
# def download():
# 	file_data=Feedback.query.filter_by(id=1).first()
# 	return send_file(BytesIO(file_data.image),attachment_filename='abc.jpg',as_attachment=True)


@app.route('/feedback')
def feedback():
    error = {"a": 2}
    if 'username' in session:
        return render_template('feedback.html')
    else:
        return render_template('login.html', error=error)


@app.route('/feedbackform', methods=['POST'])
def feedback_form():
    try:
        file = request.files["upload_file"]
        user = User.query.filter(User.rollNo == session['rollNo']).first()
        feed = Feedback(mess=request.form["mess"], date_of_issue=datetime.date.today(), issue=request.form["issue"],
                        description=request.form["description"], user_id=user.id, image=file.read())
        db.session.add(feed)
        db.session.commit()
        return "Feedback added successfully"

    except exceptions.BadRequestKeyError:
        user = User.query.filter(User.rollNo == session['rollNo']).first()
        feed = Feedback(mess=request.form["mess"], date_of_issue=datetime.date.today(), issue=request.form["issue"],
                        description=request.form["description"], user_id=user.id)
        db.session.add(feed)
        db.session.commit()
    return "Feedback added successfully"


@app.route('/daywise', methods=['POST'])
def daywise():
    # Encoding:  N - 0, S - 1, Y - 3, K - 2

    encode = {'0': 0, '1': 1, '2': 2, '3': 3}
    sun_breakfast = request.form['sun_breakfast']
    if sun_breakfast == '-1':
        sun_breakfast = False
    else:
        sun_b_mess = encode[sun_breakfast]
        sun_breakfast = True

    sun_lunch = request.form['sun_lunch']
    if sun_lunch == '-1':
        sun_lunch = False
    else:
        sun_l_mess = encode[sun_lunch]
        sun_lunch = True

    sun_dinner = request.form['sun_dinner']
    if sun_dinner == '-1':
        sun_dinner = False
    else:
        sun_d_mess = encode[sun_dinner]
        sun_dinner = True

    mon_breakfast = request.form['mon_breakfast']
    if mon_breakfast == '-1':
        mon_breakfast = False
    else:
        mon_b_mess = encode[mon_breakfast]
        mon_breakfast = True

    mon_lunch = request.form['mon_lunch']
    if mon_lunch == '-1':
        mon_lunch = False
    else:
        mon_l_mess = encode[mon_lunch]
        mon_lunch = True

    mon_dinner = request.form['mon_dinner']
    if mon_dinner == '-1':
        mon_dinner = False
    else:
        mon_d_mess = encode[mon_dinner]
        mon_dinner = True

    tue_breakfast = request.form['tue_breakfast']
    if tue_breakfast == '-1':
        tue_breakfast = False
    else:
        tue_b_mess = encode[tue_breakfast]
        tue_breakfast = True

    tue_lunch = request.form['tue_lunch']
    if tue_lunch == '-1':
        tue_lunch = False
    else:
        tue_l_mess = encode[tue_lunch]
        tue_lunch = True

    tue_dinner = request.form['tue_dinner']
    if tue_dinner == '-1':
        tue_dinner = False
    else:
        tue_d_mess = encode[tue_dinner]
        tue_dinner = True

    wed_breakfast = request.form['wed_breakfast']
    if wed_breakfast == '-1':
        wed_breakfast = False
    else:
        wed_b_mess = encode[wed_breakfast]
        wed_breakfast = True

    wed_lunch = request.form['wed_lunch']
    if wed_lunch == '-1':
        wed_lunch = False
    else:
        wed_l_mess = encode[wed_lunch]
        wed_lunch = True

    wed_dinner = request.form['wed_dinner']
    if wed_dinner == '-1':
        wed_dinner = False
    else:
        wed_d_mess = encode[wed_dinner]
        wed_dinner = True

    thu_breakfast = request.form['thu_breakfast']
    if thu_breakfast == '-1':
        thu_breakfast = False
    else:
        thu_b_mess = encode[thu_breakfast]
        thu_breakfast = True

    thu_lunch = request.form['thu_lunch']
    if thu_lunch == '-1':
        thu_lunch = False
    else:
        thu_l_mess = encode[thu_lunch]
        thu_lunch = True

    thu_dinner = request.form['thu_dinner']
    if thu_dinner == '-1':
        thu_dinner = False
    else:
        thu_d_mess = encode[thu_dinner]
        thu_dinner = True

    fri_breakfast = request.form['fri_breakfast']
    if fri_breakfast == '-1':
        fri_breakfast = False
    else:
        fri_b_mess = encode[fri_breakfast]
        fri_breakfast = True

    fri_lunch = request.form['fri_lunch']
    if fri_lunch == '-1':
        fri_lunch = False
    else:
        fri_l_mess = encode[fri_lunch]
        fri_lunch = True

    fri_dinner = request.form['fri_dinner']
    if fri_dinner == '-1':
        fri_dinner = False
    else:
        fri_d_mess = encode[fri_dinner]
        fri_dinner = True

    sat_breakfast = request.form['sat_breakfast']
    if sat_breakfast == '-1':
        sat_breakfast = False
    else:
        sat_b_mess = encode[sat_breakfast]
        sat_breakfast = True

    sat_lunch = request.form['sat_lunch']
    if sat_lunch == '-1':
        sat_lunch = False
    else:
        sat_l_mess = encode[sat_lunch]
        sat_lunch = True

    sat_dinner = request.form['sat_dinner']
    if sat_dinner == '-1':
        sat_dinner = False
    else:
        sat_d_mess = encode[sat_dinner]
        sat_dinner = True

    if not (sun_breakfast or sun_lunch or sun_dinner or mon_breakfast or mon_dinner or mon_lunch or tue_breakfast or tue_lunch or tue_dinner or wed_breakfast or wed_lunch or wed_dinner or thu_breakfast or thu_lunch or thu_dinner or fri_breakfast or fri_lunch or fri_dinner or sat_breakfast or sat_lunch or sat_dinner):
        return change(4)

    user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
    dic = json.loads(user.json)

    if mon_breakfast:
        day_needed = 1
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][mon_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if mon_lunch:
        day_needed = 1
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][mon_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if mon_dinner:
        day_needed = 1
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][3])
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][mon_d_mess] = 1
            print(dic[date_str][0][3])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if tue_breakfast:
        day_needed = 2
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][tue_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if tue_lunch:
        day_needed = 2
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][tue_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if tue_dinner:
        day_needed = 2
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][3])
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][tue_d_mess] = 1
            print(dic[date_str][0][3])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if wed_breakfast:
        day_needed = 3
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][wed_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if wed_lunch:
        day_needed = 3
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][wed_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if wed_dinner:
        day_needed = 3
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][3])
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][wed_d_mess] = 1
            print(dic[date_str][0][3])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if thu_breakfast:
        day_needed = 4
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][thu_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if thu_lunch:
        day_needed = 4
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][thu_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if thu_dinner:
        day_needed = 4
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][3])
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][thu_d_mess] = 1
            print(dic[date_str][0][3])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if fri_breakfast:
        day_needed = 5
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][fri_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if fri_lunch:
        day_needed = 5
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][fri_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if fri_dinner:
        day_needed = 5
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][3])
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][fri_d_mess] = 1
            print(dic[date_str][0][3])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sat_breakfast:
        day_needed = 6
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][0])
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][sat_b_mess] = 1
            print(dic[date_str][0][0])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sat_lunch:
        day_needed = 6
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            print(start_date_needed)
            print(dic[date_str][0][1])
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][sat_l_mess] = 1
            print(dic[date_str][0][1])
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sat_dinner:
        day_needed = 6
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][sat_d_mess] = 1
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sun_breakfast:
        day_needed = 7
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][sun_b_mess] = 1
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sun_lunch:
        day_needed = 7
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][sun_l_mess] = 1
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    if sun_dinner:
        day_needed = 7
        day_got = datetime.datetime(2019, 6, 30).isoweekday()
        diff = day_got - day_needed
        start_date_needed = (datetime.datetime(2019, 6, 30) - datetime.timedelta(days=diff)).date()
        end_date = datetime.datetime.today().date()
        while start_date_needed >= end_date:
            date_str = start_date_needed.strftime('%Y-%m-%d')
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][sun_d_mess] = 1
            new_date = start_date_needed - datetime.timedelta(days=7)
            start_date_needed = new_date

    json_mod = json.dumps(dic)
    user.json = json_mod
    db.session.commit()

    return change(0)


def init_json():
    # TODO - Modify date ranges
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
    error = {"a": 2, "status": -1}
    if 'username' in session:
        return render_template('cancel.html', error=error)
    else:
        return render_template('login.html', error=error)


@app.route('/uncancelMeal', methods=['POST'])
def uncancel_meal():
    error = {}
    date_range = request.form['date_range']
    if date_range == '':
        error["status"] = 2
        return render_template('cancel.html', error=error)
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
        error["status"] = 3
        return render_template('cancel.html', error=error)
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

        error["status"] = 1
        return render_template('cancel.html', error=error)


@app.route('/cancelMeal', methods=['POST'])
def cancel_meal():
    error = {}
    date_range = request.form['date_range']
    if date_range == '':
        error["status"] = 2
        return render_template('cancel.html', error=error)
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
        error["status"] = 3
        return render_template('cancel.html', error=error)
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

        error["status"] = 0
        return render_template('cancel.html', error=error)


@app.route('/view')
def view():
    if 'username' in session:
        user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
        dic = json.loads(user.json)
        breakfast_dict = {}
        lunch_dict = {}
        dinner_dict = {}

        start_date_str = '01/07/2018'
        start_date = start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y').date()
        date_count = 364
        while date_count > -1:
            date = start_date + datetime.timedelta(days=date_count)
            date_str = date.strftime('%Y-%m-%d')
            new_date_str = date.strftime('%m/%d/%Y')
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    if i == 0:
                        breakfast_dict[new_date_str] = 'Breakfast - North'
                    elif i == 1:
                        breakfast_dict[new_date_str] = 'Breakfast - South'
                    elif i == 2:
                        breakfast_dict[new_date_str] = 'Breakfast - Kadamb'
                    elif i == 3:
                        breakfast_dict[new_date_str] = 'Breakfast - Yuktahar'
                elif dic[date_str][0][0][i] == -1:
                    breakfast_dict[new_date_str] = 'Breakfast - Cancelled'

            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    if i == 0:
                        lunch_dict[new_date_str] = 'Lunch - North'
                    elif i == 1:
                        lunch_dict[new_date_str] = 'Lunch - South'
                    elif i == 2:
                        lunch_dict[new_date_str] = 'Lunch - Kadamb'
                    elif i == 3:
                        lunch_dict[new_date_str] = 'Lunch - Yuktahar'
                elif dic[date_str][0][1][i] == -1:
                    lunch_dict[new_date_str] = 'Lunch - Cancelled'

            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    if i == 0:
                        dinner_dict[new_date_str] = 'Dinner - North'
                    elif i == 1:
                        dinner_dict[new_date_str] = 'Dinner - South'
                    elif i == 2:
                        dinner_dict[new_date_str] = 'Dinner - Kadamb'
                    elif i == 3:
                        dinner_dict[new_date_str] = 'Dinner - Yuktahar'
                elif dic[date_str][0][3][i] == -1:
                    dinner_dict[new_date_str] = 'Dinner - Cancelled'

            date_count -= 1
        # print(breakfast_dict['12/15/2018'], "asdasdas")
        return render_template('view.html', breakfast_dict=breakfast_dict, lunch_dict=lunch_dict,
                               dinner_dict=dinner_dict)
    else:
        error = {"a": 2}
        return render_template('login.html', error=error)


# @app.route('/change')
# def change():
# 	return render_template('change.html')

@app.route('/change')
def change(status=-1):
    if 'username' in session:
        print(status)
        Y = {}

        time = ["breakfast", "lunch", "snacks", "dinner"]
        day = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        mess = ["north", "south", "yuktahar", "kadamb"]

        menus = Menu.query.all()
        t = 0
        d = 0
        m = 0

        for menu in menus:
            st = "item" + str(d) + str(t) + str(m)
            s = st + str(1)
            Y[s] = menu.item1
            s = st + str(2)
            Y[s] = menu.item2
            s = st + str(3)
            Y[s] = menu.item3
            s = st + str(4)
            Y[s] = menu.item4
            s = st + str(5)
            Y[s] = menu.item5
            s = st + str(6)
            Y[s] = menu.item6
            s = st + str(7)
            Y[s] = menu.item7
            s = st + str(8)
            Y[s] = menu.item8
            s = st + str(9)
            Y[s] = menu.item9
            s = st + str(10)
            Y[s] = menu.item10
            s = st + str(11)
            Y[s] = menu.item11
            s = st + str(12)
            Y[s] = menu.item12
            m = m + 1
            if m == 4:
                m = 0
                t = t + 1
            if t == 4:
                t = 0
                d = d + 1
        error = {"status": status}
        # if status==0:
        #     error["status"] = 0
        # elif status==1:
        #     error["status"] = 1
        # elif status==2:
        #     error["status"] = 2
        # else:
        #     error["status"] = -1

        return render_template('change.html', Y=Y, error=error)
    else:
        error = {"a": 2}
        return render_template('login.html', error=error)


@app.route('/changeMeal', methods=['POST'])
def change_meal_date():
    date_range = request.form['date_range']
    if date_range == '':
        return change(3)
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
        return change(2)
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
    return change(0)


@app.route('/change_meal_month', methods=['POST'])
def change_meal_month():
    error = {}
    month = request.form['select_month']
    if month == '':
        return change(1)
    else:
        month_string, year_string = month.split(', ')
        month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                      'September': 9, 'October': 10, 'November': 11, 'December': 12}
        week_day_number, number_of_days = monthrange(int(year_string), month_dict[month_string])
        start_date_string = "1/" + str(month_dict[month_string]) + "/" + year_string
        start_date = datetime.datetime.strptime(start_date_string, '%d/%m/%Y').date()
        date_count = number_of_days - 1
        end_date = start_date + datetime.timedelta(days=date_count)
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
    if not (breakfast or lunch or dinner):
        return change(2)

    user = User.query.filter(and_(User.rollNo == session['rollNo'])).first()
    dic = json.loads(user.json)

    while date_count > -1:
        date = start_date + datetime.timedelta(days=date_count)
        date_str = date.strftime('%Y-%m-%d')
        if breakfast:
            for i in range(len(dic[date_str][0][0])):
                if dic[date_str][0][0][i] == 1:
                    dic[date_str][0][0][i] = 0
            dic[date_str][0][0][mess_number] = 1

        if lunch:
            for i in range(len(dic[date_str][0][1])):
                if dic[date_str][0][1][i] == 1:
                    dic[date_str][0][1][i] = 0
            dic[date_str][0][1][mess_number] = 1

        if dinner:
            for i in range(len(dic[date_str][0][3])):
                if dic[date_str][0][3][i] == 1:
                    dic[date_str][0][3][i] = 0
            dic[date_str][0][3][mess_number] = 1
        date_count -= 1

    json_mod = json.dumps(dic)
    user.json = json_mod
    db.session.commit()
    return change(0)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route('/registerNext', methods=['GET', 'POST'])
def registerNext():
    try:
        user = User(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"],
                    rollNo=request.form["rollNo"], password=sha256_crypt.encrypt(request.form['loginPassword']),
                    json=init_json())
        db.session.add(user)
        db.session.commit()
    except:
        error = {"a": 3}
        return render_template('login.html', error=error)
    return redirect(url_for('index'))


@app.route('/loginNext', methods=['GET', 'POST'])
def loginNext():
    error = {"a": 1}
    print(error["a"])
    if request.method == "POST":
        rollNo = request.form['rollNo']
        password = request.form['loginPassword']

        user = User.query.filter(User.rollNo == rollNo).first()

        if user:
            if sha256_crypt.verify(password, user.password):
                session['username'] = user.firstname
                session['rollNo'] = user.rollNo
                session['email'] = user.email
                return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        name = session.pop('username')
        email = session.pop('email')
        roll_no = session.pop('rollNo')

    return redirect(url_for('index'))


@app.route('/admin/register')
@app.route('/admin/login')
@app.route('/admin/index')
@app.route('/admin/')
def adminIndex():
    if 'adminID' in session:
        return render_template('adminChange.html')
    else:
        error = {}
        return render_template('adminLogin.html', error=error)


@app.route('/admin/registerNext', methods=['GET', 'POST'])
def adminRegisterNext():
    try:
        admin = Admin(firstname=request.form["fname"], lastname=request.form["lname"], email=request.form["email"],
                      mess=request.form["mess"], adminID=request.form["adminID"],
                      password=sha256_crypt.encrypt(request.form['loginPassword']))
        db.session.add(admin)
        db.session.commit()
    except:
        return "Error: Please check for following errors: <br />1. Email<br />2.Admin ID"
    return redirect(url_for('adminIndex'))


@app.route('/admin/loginNext', methods=['GET', 'POST'])
def adminLoginNext():
    if request.method == "POST":
        adminID = request.form['adminID']
        password = request.form['loginPassword']

        admin = Admin.query.filter(Admin.adminID == adminID).first()

        if admin:
            if sha256_crypt.verify(password, admin.password):
                session['firstName'] = admin.firstname
                session['mess'] = admin.mess
                session['adminID'] = admin.adminID
                session['email'] = admin.email
                return redirect(url_for('adminIndex'))
        return "Invalid Username or Password"


@app.route('/admin/logout', methods=['POST', 'GET'])
def adminLogout():
    if 'adminID' in session:
        name = session.pop('firstName')
        email = session.pop('email')
        mess = session.pop('mess')
        adminID = session.pop('adminID')
    return redirect(url_for('adminIndex'))


# @app.route('/img/<int:img_id>')
# def serve_img(img_id):
#     pass 

@app.route('/admin/feedback', methods=['POST', 'GET'])
def adminFeedback():
    if 'adminID' in session:
        feed=Feedback.query.filter(Feedback.mess==session['mess']).all()
        for f in feed:
            f.rollNo = User.query.filter(User.id == f.user_id).first().rollNo
            f.firstname = User.query.filter(User.id == f.user_id).first().firstname
            if f.image:
                f.image = f.image.decode('base64')
        return render_template('adminFeedback.html', feedback=feed)
    else:
        return redirect(url_for('adminIndex'))


# file_data=Feedback.query.filter_by(id=1).first()
# return send_file(BytesIO(file_data.image),attachment_filename='abc.jpg',as_attachment=True)


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

    menus = Menu.query.filter(Menu.mess == session['mess']).all()

    return render_template('adminChange.html', menus=menus)


@app.route('/admin/changeMenu', methods=['GET', 'POST'])
def adminChangeMenu():
    menu = Menu.query.filter((Menu.time == request.form['time']) and (Menu.day == request.form['day']) and (
            Menu.mess == session['mess'])).first()

    menu.item1 = request.form['item1']
    menu.item2 = request.form['item2']

    if request.form['time'] == "snacks":
        menu.item3 = menu.item4 = menu.item5 = menu.item6 = menu.item7 = "NA"
        menu.item8 = menu.item9 = menu.item10 = menu.item11 = menu.item12 = "NA"
    else:
        menu.item3 = request.form['item3']
        menu.item4 = request.form['item4']
        menu.item5 = request.form['item5']
        menu.item6 = request.form['item6']
        menu.item7 = request.form['item7']
        menu.item8 = request.form['item8']
        if request.form['time'] == "breakfast":
            menu.item9 = menu.item10 = menu.item11 = menu.item12 = "NA"
        else:
            menu.item9 = request.form['item9']
            menu.item10 = request.form['item10']
            menu.item11 = request.form['item11']
            menu.item12 = request.form['item12']

    db.session.commit()

    return "Menu Changed successfully"


@app.route('/admin/rates')
def adminRates():
    # mess = ["north", "south", "yuktahar", "kadamb"]
    # time = ["breakfast", "lunch", "snacks", "dinner"]
    # rate = ["30", "50", "20", "50"]

    # for m in mess:
    #     for i in range(0, len(time)):
    #         r = Rates(mess=m, time=time[i], rate=rate[i])
    #         db.session.add(r)
    #         db.session.commit()

    rates = Rates.query.filter(Rates.mess == session['mess']).all()

    return render_template('adminRates.html', rates=rates)


@app.route('/admin/changeRates', methods=['GET', 'POST'])
def adminChangeRates():
    r = Rates.query.filter((Rates.mess==session['mess']) and (Rates.time == request.form['time'])).first()

    r.rate = request.form['rate']

    db.session.commit()

    return "Rate Changed successfully"
