from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

