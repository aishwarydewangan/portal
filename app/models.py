from datetime import datetime
from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	rollNo = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)
	json = db.Column(db.Unicode, nullable=True)
	feedback=db.relationship('Feedback',backref='user',lazy=True)
	
	def __repr__(self):
		return "User('{self.email}')"

class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	mess = db.Column(db.String(30), unique=True, nullable=False)
	adminID = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return "Admin('{self.email}')"

class Menu(db.Model):
	mess = db.Column(db.String(30), primary_key=True, nullable=False)
	time = db.Column(db.String(30), primary_key=True, nullable=False)
	day = db.Column(db.String(30), primary_key=True, nullable=False)
	item1 = db.Column(db.String(30), nullable=False)
	item2 = db.Column(db.String(30), nullable=False)
	item3 = db.Column(db.String(30), nullable=False)
	item4 = db.Column(db.String(30), nullable=False)
	item5 = db.Column(db.String(30), nullable=False)
	item6 = db.Column(db.String(30), nullable=False)
	item7 = db.Column(db.String(30), nullable=False)
	item8 = db.Column(db.String(30), nullable=False)
	item9 = db.Column(db.String(30), nullable=False)
	item10 = db.Column(db.String(30), nullable=False)
	item11 = db.Column(db.String(30), nullable=False)
	item12 = db.Column(db.String(30), nullable=False)


class Rates(db.Model):
	mess = db.Column(db.String(30), primary_key=True, nullable=False)
	time = db.Column(db.String(30), primary_key=True, nullable=False)
	rate = db.Column(db.String(30), nullable=False)


class Feedback(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	mess=db.Column(db.String(60), nullable=False)
	date_of_issue=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	issue=db.Column(db.Text,nullable=False)
	description=db.Column(db.Text,nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	image=db.Column(db.LargeBinary,nullable=True)

	def __repr__(self):
		return "Feedback('{self.content}')"




db.create_all()