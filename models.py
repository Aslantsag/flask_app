from flask import Flask, render_template, url_for, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///line.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(50), nullable=False)
    u_phone = db.Column(db.String(11), nullable=False, default='Без имени')
    secret_key = db.Column(db.String(36), nullable=False)
    status = db.Column(db.Integer, default=1)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Posts %>' % self.id