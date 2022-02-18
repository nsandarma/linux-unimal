from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fasisme123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://zpmcpkdjdiijyz:75f91ce972f4daf08ddedb62010cb87d1f7543064c19d0ba1c9520c18340b2cd@ec2-107-20-24-247.compute-1.amazonaws.com:5432/d1vn30f8o03smk"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=15)

db = SQLAlchemy(app=app)

login = LoginManager(app)
login.login_view='login'


from app.models import *
from app.routes import *
