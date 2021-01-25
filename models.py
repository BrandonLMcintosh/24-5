from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import session

bcrypt = Bcrypt()

db = SQLAlchemy()



def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    def __repr__(self):
        return f"""
        ID - {self.username},
        Password - {self.password},
        Email - {self.email}, 
        First_name - {self.first_name},
        Last_name - {self.last_name}
        """

    username = db.Column(db.Text, nullable=False, unique=True, primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    @property
    def dict_version(self):

        return {
            "id":self.id,
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name
        }


    @classmethod
    def hash_password(cls, password):

        return bcrypt.generate_password_hash(password)


    @classmethod
    def compare_hash(cls, password, hash):

        return bcrypt.check_password_hash(hash, password)


    @classmethod
    def register(cls, form):

        user = cls(
            username=form.username.data, 
            password=cls.hash_password(form.password.data),
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
            )

        db.session.add(user)
        db.session.commit()

        db_user = cls.query.filter_by(username=form.username.data)

        response = {
            "registered":db_user.dict_version
        }

        session['username'] = db_user.username

        return response


    @classmethod
    def login(cls, form):

        user = cls.query.filter_by(username=form.username.data).first()

        if cls.compare_hash(form.password.data, user.password):

            session['username'] = user.username

            return {
                'logged_in': user.dict_version
            }

        else:

            return {
                "error": "Bad username/password"
            }

    @classmethod
    def is_authenticated():
        return 

    @classmethod
    def logout(cls):

        del session['user_id']

        return {
            "logged_out": True
        }