from enum import unique
from app import db,UserMixin

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.Integer,nullable=False)
    role = db.Column(db.Integer,nullable=False)
    content = db.Column(db.String)

    def __repr__(self) -> str:
        if int(self.role) == 1:
            return f'<Role = admin>'
        else:
            return f'Role = user>'
# class Message(db.Model):
#     __tablename__ = 'message'
#     id = db.Column(db.Integer,primary_key=True)
#     usename = db.Column(db.String,db.ForeignKey('user.username'))
#     content = db.Column(db.String,nullable=False)


