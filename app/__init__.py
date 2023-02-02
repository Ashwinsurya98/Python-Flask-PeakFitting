from flask import *
from flask_session import Session
app=Flask(__name__)
from app import views
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
