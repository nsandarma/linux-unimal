from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fasisme123'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://wupncvuwdmjpsq:f48a01be5ed9a99b046cf7ef517bc832eb0abc9725b3d6b1f151b1b77aa156b5@ec2-3-224-157-224.compute-1.amazonaws.com:5432/d1ntjkfg5kgj8n"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=15)


db = SQLAlchemy(app=app)


login = LoginManager(app)
login.login_view='login'


from app.models import *
from app.routes import *
