import json
from re import M
from sqlalchemy.orm import query
from app import app,render_template,request,db,User,login,login_required,login_user,logout_user,url_for,redirect,session
from werkzeug.security import generate_password_hash,check_password_hash


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    if session.get('key'):
        data = {'nama':'admin'}
    else:
        data = {'nama':'user'}
    
    ha = session.get("hash")
    user = User.query.filter_by(username=ha).first()
    message = json.loads(user.content)
    return render_template("landing.html",value=data,hashing=ha,data=message)

@app.route('/login',methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            try:
                q = User.query.filter_by(username=username).first()
                if check_password_hash(q.password,password):
                    if int(q.role) == 1:
                        login_user(q)
                        session['key'] = True
                        return redirect(url_for('index'))
                    else:
                        login_user(q)
                        session['key'] = False

                        session['hash'] = f"{q.username}"
                        return redirect('/')
                else:
                    a = "Username atau password salah ! "
                    return render_template('login.html',data = a)
            except Exception as e:
                a = "Username atau password salah ! "
                return render_template('login.html',data = a)
    return render_template('login.html')
@app.route('/index')
@login_required
def index():
    if session.get('key'):
        data = User.query.all()
        return render_template('index.html',value=data)
    else:
        return "anda harus masuk sebagai admin"

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            try:
                pass_hash = generate_password_hash(password)
                if username == 'root':    
                    q = User(username=username,password=pass_hash,role=1)
                    db.session.add(q)
                    db.session.commit()
                    return redirect('/login')
                else:
                    a = json.dumps([])
                    q = User(username=username,password=pass_hash,role=0,content=a)

                    db.session.add(q)
                    db.session.commit()
                    return redirect('/login')
            except Exception as e:
                return f'error {e}'

    return render_template('register.html')

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        q = User.query.filter_by(id=id).first()
        if int(q.role) != 1 :
            db.session.delete(q)
            db.session.commit()
            return redirect('/index')
        else :
            return "anda tidak bisa menghapus role admin"
        
    except Exception as e:
        return f'{e}'

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

@app.route('/message/<string:hashing>',methods=["GET","POST"])
def send_message(hashing):
  
    a = User.query.filter_by(username=hashing).first()
    if session.get('hash') == hashing  or not a:
        return f"Not Working or username not detected !! {a}"
    else:
        try :
            if request.method == 'POST':
                message = request.form['message']
                user = User.query.filter_by(username=hashing).first()
                v = json.loads(user.content)
                v.append(message)
                user.content = json.dumps(v)
                db.session.commit()
                return render_template('template/form_message.html')
            
            return render_template('template/form_message.html')
        except Exception as e:
            return f"{e}"

@app.route('/delmessage/<string:message>')
@login_required
def del_message(message):
    ha = session.get('hash')
    q = User.query.filter_by(username=ha).first()
    content = json.loads(q.content)
    content.remove(message)
    q.content = json.dumps(content)
    db.session.commit()
    return redirect('/')

@app.route('/message/')
@login_required
def message():
    ha = session.get('hash')
    q = User.query.filter_by(username=ha).first()
    content = json.loads(q.content)
    return render_template('template/table_message.html',message=content)



    

