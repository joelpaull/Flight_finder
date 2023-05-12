import sqlite3

class UserManager():
    
    def __init__(self) -> None:
        pass
    
    def add_user(self, username, password, db_path):
        with sqlite3.connect(db_path) as db:
            data = (db.execute("SELECT * FROM flights")).fetchall()
            print(data)