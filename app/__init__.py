from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fasisme123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=15)


db = SQLAlchemy(app=app)


login = LoginManager(app)
login.login_view='login'


from app.models import *
from app.routes import *
