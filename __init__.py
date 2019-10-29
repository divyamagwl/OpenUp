from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

class Confession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    for_whom = db.Column(db.String(100))
    description = db.Column(db.Text)
    identity = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime)


@app.route('/')
def index():
    return redirect(url_for('login'))

global username
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    global username
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        login = User.query.filter_by(username=username, password=password).first()
        if login is None:
            error = 'Invalid Credentials. Please Try again.'
        else:
            return redirect(url_for('home'))
                
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        register = User(username = username, password = password)
        
        if not username :
            error = 'Username is required'
        elif not password :
            error = 'Password is required'
        else:
            if User.query.filter_by(username=username).first():
                error = 'Username already taken'
            else:
                db.session.add(register)
                db.session.commit()
                return redirect(url_for("login"))

    return render_template("register.html", error = error) 

@app.route('/home')
def home():
    confessions = db.session.query(Confession).all()
    return render_template("home.html", confessions = confessions)

@app.route('/add' , methods =['GET','POST'])
def add():
    if request.method == 'POST' :
        for_whom = request.form.get('for_whom')
        description = request.form.get('description')
        identity = request.form.get('identity')
        creation_time = datetime.now()

        new_confession = Confession(for_whom = for_whom , description = description, identity=identity, creation_time=creation_time) 
        db.session.add(new_confession)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('add.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
