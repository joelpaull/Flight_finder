import requests
import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import os.path
from helpers.user_manager import UserManager, login_required
from helpers.flight_search import FlightSearch


IATA_API = "https://api.tequila.kiwi.com/locations/query"
IATA_KEY = "_TdJlNEcqHgkQQ6JDdN_ftjKx_WBGfK_"


# Configure Flask 
app = Flask(__name__)
app.secret_key = 'jp1996'

# Configure database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "flights.sqlite")

# Create object from classes
user_manager = UserManager()
flight_search = FlightSearch()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Direct to Login 
@app.route("/")
def index():
    print(session.get("username"))
    if session.get("username") == None:
        return redirect("/login")
    else:
        return redirect("/homepage")


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
            return render_template("homepage.html")
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
        phone_number = request.form.get("phone_number")

        if username == "" or password == "" or pass_confirmation == "" or phone_number == "":
            error = "Please Ensure All Registration Details Are Entered."
            return render_template("error.html", error = error)

        # Check username not taken & passwords match. Then add to database 
        if password == pass_confirmation:
                
                # user_added returns False if username taken.
                user_added = user_manager.add_user(username, password, phone_number, DB_PATH)
                if user_added:
                     return render_template("register_success.html", username = username)
                else:
                    error = "Username Taken."
                    return render_template("error.html", error = error)
        else:
            error = "Passwords Do Not Match."
            return render_template("error.html", error = error)
        

@app.route("/logout")
def logout():
    '''Log user out'''

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
        

@app.route("/homepage")
def homepage():
    print(session)
    return render_template("homepage.html")

@app.route("/add_flight")
def add_flight():
    return render_template("add_flight.html")

@app.route("/iata", methods = ["GET", "POST"])
def iata():

    # If form posted; make API call to retrieve IATA code.
    if request.method == "POST":
        name = request.form.get("name")
        IATA = flight_search.get_IATA(name)

        # Save search to searches database
        flight_search.log_search(name, IATA, DB_PATH)
        
        # Return user page to show search response
        return render_template("IATA_response.html", IATA = IATA, name = name.capitalize())


    else:    
        return render_template("IATA.html")


