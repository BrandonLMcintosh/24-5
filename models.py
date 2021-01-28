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
        Username - {self.username},
        Password - {self.password},
        Email - {self.email}, 
        First_name - {self.first_name},
        Last_name - {self.last_name}
        """

    username = db.Column(db.Text, nullable=False, unique=True, primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(), nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    @property
    def dict_version(self):

        response = {
            "username":self.username,
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name
        }

        return response


    @staticmethod
    def hash_password(password):

        hashed_password = bcrypt.generate_password_hash(password, 14)
        decoded_password = hashed_password.decode('utf8')

        return decoded_password


    @staticmethod
    def encode_password(password):

        encoded_password = password.encode('utf8')

        return encoded_password


    @classmethod
    def register(cls, form, username=None, password=None, email=None, first_name=None, last_name=None):
        query_username = None
        if form:
            
            user = cls(
                username=form.username.data, 
                password=cls.hash_password(cls.encode_password(form.password.data)),
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
                )

            query_username = form.username.data

        else:
            user = cls(
                username=username, 
                password=cls.hash_password(cls.encode_password(password)),
                email=email,
                first_name=first_name,
                last_name=last_name
                )
            query_username = username
            

        db.session.add(user)
        db.session.commit()

        db_user = cls.query.filter_by(username=query_username).first()

        response = {
            "registered":db_user.dict_version
        }

        session['username'] = db_user.username

        return response


    @classmethod
    def login(cls, form):

        user = cls.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, cls.encode_password(form.password.data)):

            session['username'] = user.username

            return True

        else:

            return False


    @staticmethod
    def is_authenticated():
        if 'username' in session:
            return True
        else:
            return False


    @classmethod
    def logout(cls):

        del session['user_id']

        return {
            "logged_out": True
        }


    @classmethod
    def delete(cls, username):

        user = cls.get(username)

        db.session.delete(user)
        db.session.commit()


    @classmethod
    def get(cls, username):

        user = cls.query.filter_by(username=username).first()

        return user

class Feedback(db.Model):

    __tablename__ = "feedback"

    def __repr__(self):
        representation = f"""
            ID: {self.id}, 
            Title: {self.title},
            Content: {self.content},
            Username: {self.username}
        """

        id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)
        username = db.relationship('User', backref='feedback')

    @classmethod
    def add(cls, username, form=None, title=None, content=None):

        if form:

            feedback = cls(title=form.title.data, content=form.content.data, username=username)
        
        else:

            feedback = cls(title=form.title.data, content=form.content.data, username=username)

        db.session.add(feedback)
        db.session.commit()


    @classmethod
    def update(cls, username, form_id, form=None, title=None, content=None):

        feedback = cls.query.get_or_404(form_id)
        
        if form:

            feedback.title=form.title.data
            feedback.content=form.content.data
        
        else:

            feedback.title=title
            feedback.content=content
        
        db.session.add(feedback)
        db.session.commit()

    
    @classmethod
    def delete(cls, id):

        feedback = cls.query.get_or_404(id)

        db.session.delete(feedback)
        db.session.commit()

        