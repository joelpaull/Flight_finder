import requests
import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import os.path
from helpers.user_manager import UserManager, login_required


# Configure Flask 
app = Flask(__name__)
app.secret_key = 'jp1996'

# Configure database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "flights.sqlite")

# Create user_manager object
user_manager = UserManager()


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Clear any current user sessions
    session.clear()

    # Allow user to login
    if request.method == "GET":
        ''' Allow user to Login'''
        return render_template("login.html")
    
    else:
        # Retrieve details from posted form if POST
        username = request.form.get("username")
        password = request.form.get("password")

        # Check database for user details
        valid_user = user_manager.check_user(username, password, DB_PATH)

        # if username in database and password matches, log user in
        if valid_user:
            session["username"] = username
            return render_template("/homepage")
        else:
            # TODO
            return render_template("error.html")

    

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        ''' Allow user to Register'''
        return render_template("register.html")
    
    # Retrieve details from posted form if POST
    else: 
        username = request.form.get("username")
        password = request.form.get("password")
        pass_confirmation = request.form.get("confirmation")

        # Check passwords match and add to database 
        if password == pass_confirmation:
            user_added = user_manager.add_user(username, password, DB_PATH)
        else:
            error = "Sorry, Passwords Do Not Match."
            render_template("error.html", error = error)

        # Show result of user addition
        if user_added:
            render_template("register_success.html", username = username)
        else:
            # TODO
            error = "Username Taken."
            return render_template("error.html", error = error)
        

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")



