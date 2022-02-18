from app import db,UserMixin
import requests as req
import json as js


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.Integer,nullable=False)
    content = db.Column(db.String)

    def __repr__(self) -> str:
        if int(self.role) == 1:
            return f'<Role = admin>'
        else:
            return f'Role = user>'

def get_data():
    r = req.get('https://disease.sh/v3/covid-19/countries/idn')
    return r.json()
