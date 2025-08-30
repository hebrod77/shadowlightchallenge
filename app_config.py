from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from environment import *
from os import environ

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DB_NAME
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)