import sqlite3

class UserManager():

    def __call__(self):
        pass
    
    def add_user(self, username, password, db_path):
        with sqlite3.connect(db_path) as db:
            db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
            