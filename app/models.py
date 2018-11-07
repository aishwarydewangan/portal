from datetime import datetime
from app import db

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    rollNo = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    messFile=db.Column(db.String(35), nullable=True)

    def __repr__(self):
        return "Login('{self.email}')"

db.create_all()


