from app.models import db

if __name__ == '__main__':
    db.create_all()
    print("success")