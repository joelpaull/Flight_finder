#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import sqlite3
from flask import Flask, redirect, render_template
import os.path


# Configure Flask 
app = Flask(__name__)

# Configure database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "flights.sqlite")
db = sqlite3.connect(db_path) 

