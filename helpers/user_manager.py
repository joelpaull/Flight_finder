import sqlite3
from flask import redirect, render_template, request, session
from functools import wraps

class UserManager():  

    def check_user(self, username, password, db_path):
        '''Query DB for username and check password matches'''
        with sqlite3.connect(db_path) as db:
            row = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchall()
            if len(row) != 1 or password != row[0][1]:
                return False
            return True
    

    def add_user(self, username, password, phone_number, db_path):
        ''' Add user, returns false is username taken'''
        with sqlite3.connect(db_path) as db:
            try:
                db.execute("INSERT INTO user (username, password, phone_number) VALUES (?, ?, ?)", (username, password, phone_number))
            except sqlite3.IntegrityError:
                return False
        return True


def login_required(f):
# Decorate routes to require login. https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function