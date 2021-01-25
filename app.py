from forms import Login_Form
from flask import Flask, request, redirect, jsonify, render_template, flash, session
from models import User
from secret_key import secret_key
from seed import seed_db
from forms import Login_Form, Register_Form

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

seed_db(app)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods = ["GET", "POST"])
def register():

    form = Login_Form()

    if request.method == "GET":

        return render_template('register.html.j2', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():

            User.register(form)

            return redirect('/login')

        else:

            form.username.errors = ['Invalid entries']

            return render_template('register.html.j2', form=form)
            
    else:

        flash('something went wrong')

        return redirect('/register')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login_Form()

    if request.method == "GET":

        return render_template('login.html.j2', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():

            User.login(form)

            return redirect('/secret')

        else:
            
            form.username.errors = ['Bad username/password']

            return render_template('/login', form=form)

    else: 

        flash('something went wrong')

        return redirect('/login')

@app.route('/secret')
def secret():
    
    return render_template('secret.html.j2')