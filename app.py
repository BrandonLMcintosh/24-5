from forms import Feedback_Form, Login_Form
from flask import Flask, request, redirect, jsonify, render_template, flash, session
from models import User, Feedback, connect_db, db
from secret_key import secret_key
from seed import seed_db
from forms import Login_Form, Register_Form, Feedback_Form

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.before_first_request
def resetDB():

    db.drop_all()
    db.create_all()

    seed_db(app)


@app.route('/')
def index():

    return redirect('/register')


@app.route('/register', methods = ["GET", "POST"])
def register():

    form = Register_Form()

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

            response = User.login(form)
            if response:
                
                return redirect('/secret')
            
            else: 
                
                flash("Bad username / Password")
                return redirect('/login')

        else:
            
            form.username.errors = ['Bad username/password']

            return render_template('/login', form=form)

    else: 

        flash('something went wrong')

        return redirect('/login')


@app.route('/logout')
def logout():

    del session['username']

    return redirect('/login')


@app.route('/users/<username>')
def secret():

    if User.is_authenticated():

        return render_template('secret.html.j2')
        
    else: 

        flash('You need to be logged in to view that page')

        return redirect('/login')


@app.route('/users/<username>')
def feedback_add(username):

    if User.is_authenticated():

        

        return render_template('feedback/add.html.j2')
    
    elif request.method == "POST":

        if form.validate_on_submit():

            Feedback.add(username, form=form)
            
            return redirect(f'/user/{username}')

        else: 
            
            flash('Please correct any errors in this form')

            return render_template('feedback/add.html.j2', form=form, username=username)
    
    else: 

        flash("something went wrong")

        return redirect(f'/user/{username}')


@app.route('/user/<username>/delete')
def feedback_update(username):

    if User.is_authenticated() and session['username'] == username:

        User.delete(username)

        return redirect('/register')

    else:

        flash('You must be logged in to do this.')

        return redirect('/login')
        