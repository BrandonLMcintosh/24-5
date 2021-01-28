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


# @app.before_first_request
# def resetDB():

#     db.drop_all()
#     db.create_all()

#     seed_db(app)


@app.route('/')
def index():

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def user_register():

    form = Register_Form()

    if request.method == "GET":

        return render_template('user/register.html.j2', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():

            User.register(form)

            return redirect('/login')

        else:

            form.username.errors = ['Invalid entries']

            return render_template('user/register.html.j2', form=form)

    else:

        flash('something went wrong')

        return redirect('/register')


@app.route('/login', methods=["GET", "POST"])
def user_login():

    form = Login_Form()

    if request.method == "GET":

        return render_template('user/login.html.j2', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():

            response = User.login(form)
            if response:

                username = session['username']
                return redirect(f'/users/{username}')

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
def user_logout():

    User.logout()

    return redirect('/login')


@app.route('/users/<username>')
def user_get(username):

    if User.is_authenticated():

        user = User.get(username)

        print(user.feedbacks)

        return render_template('user/get.html.j2', user=user)

    else:

        flash("You must be logged in to access this page")

        return redirect(f'/login')


@app.route('/users/<username>/delete')
def user_delete(username):

    if User.is_authenticated() and session['username'] == username:

        User.delete(username)

        return redirect('/login')

    else:

        flash('You need to be logged in to do that')

        return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def feedback_add(username):

    form = Feedback_Form()

    if User.is_authenticated():

        if request.method == "GET":

            return render_template('/feedback/add.html.j2', form=form, username=username)

        elif request.method == "POST":

            Feedback.add(username, form=form)

            return redirect(f'/users/{username}')

        else:

            flash("something went wrong")

            return redirect(f'/users/{username}')

    else:

        flash('You must be logged in to do this.')

        return redirect('/login')


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def feedback_update(feedback_id):

    feedback = Feedback.get(feedback_id)

    if User.is_authenticated() and session['username'] == feedback.username:

        form = Feedback_Form(obj=Feedback.get(feedback_id))

        if request.method == "GET":

            return render_template('feedback/update.html.j2', form=form, feedback=feedback)

        elif request.method == "POST":

            print('*'*40)
            print(form.title.data)

            Feedback.update(feedback_id, form=form)

            return redirect(f'/users/{feedback.username}')

        else:

            flash('Something went wrong.')

            return redirect(request.referrer)
    else:

        flash('You must be logged in to do this')

        return redirect('/login')


@app.route('/feedback/<int:feedback_id>/delete')
def feedback_delete(feedback_id):

    feedback = Feedback.get(feedback_id)

    if User.is_authenticated() and session['username'] == feedback.username:

        Feedback.delete(feedback_id)

        return redirect(request.referrer)
    else:

        flash("You must be logged in to do that")

        return redirect('/login')
