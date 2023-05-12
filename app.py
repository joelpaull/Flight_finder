#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import sqlite3
from flask import Flask, redirect, render_template
import os.path
from user_manager import UserManager


# Configure Flask 
app = Flask(__name__)

# Configure database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "flights.sqlite")

# Create user_manager object
user_manager = UserManager()
user_manager.add_user("wfw","wef", DB_PATH)
current_user = ""


@app.route("/")
def index():
    return redirect("/login")

@app.route("/login")
def login():
    ''' Allow user to Login'''
    if current_user == "":
        return render_template("login.html")
    
    # Else show homepage
    
@app.route("/register")
def register():
    pass



