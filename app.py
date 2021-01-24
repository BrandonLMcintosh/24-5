from flask import Flask, request, jsonify, render_template
from models import User
from secret_key import secret_key
from seed import seed_db

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

seed_db(app)

