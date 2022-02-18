import json
from app import app,render_template,request,db,User,login,login_required,login_user,logout_user,url_for,redirect,session,get_data
from werkzeug.security import generate_password_hash,check_password_hash
from time import strftime


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    ha = session.get("hash")
    user = User.query.filter_by(username=ha).first()
    if session.get('key'):
        data = {'nama':'admin'}
        message = []    
    else:
        data = {'nama':'user'}
        message = json.loads(user.content)
    return render_template("landing.html",value=data,hashing=ha,data=message,covid=get_data())

@app.route('/login',methods=['GET','POST'])
def login():
    session.clear()
    lead = "anda harus login dulu ya"
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
                    return render_template('login.html',data = a,i =lead)
            except Exception as e:
                a = "Username atau password salah ! "
                return render_template('login.html',data = a,i=lead)
    return render_template('login.html',i = lead)
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
    lead = "anda sudah keluar ! "
    return render_template('login.html',i = lead)

@app.route('/message/<string:hashing>',methods=["GET","POST"])
def send_message(hashing):
  
    a = User.query.filter_by(username=hashing).first()
    if session.get('hash') == hashing  or not a:
        return f"Not Working or username not detected !! {a}"
    else:
        try :
            if request.method == 'POST' :
                message = request.form['message']
                v = json.loads(a.content)
                date = strftime("%Y-%m-%d %H:%M:%S")
                user = session.get('hash')
                if user == None :
                    user = "anonymous"
                isi = {'date': date,'message':message,'pengirim':session.get('hash')}
                v.append(isi)
                a.content = json.dumps(v)
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
    return redirect('/message')

@app.route('/message/')
@login_required
def message():
    try :
        ha = session.get('hash')
        q = User.query.filter_by(username=ha).first()
        content = json.loads(q.content)
        return render_template('template/table_message.html',message=content)
    except :
        
        return "Nothing page ! Sorry :)"

@app.route('/test')
def tes():
    q = User.query.filter_by(username='sandy').first()
    
    try:
        return f"{q.content}"
    except Exception as e:
        return f"{e}"


    

