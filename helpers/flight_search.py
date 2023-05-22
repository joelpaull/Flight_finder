import requests
import sqlite3

IATA_API = "https://api.tequila.kiwi.com/locations/query"
IATA_KEY = "_TdJlNEcqHgkQQ6JDdN_ftjKx_WBGfK_"


class FlightSearch:

    def get_IATA(self, name):
        '''Retrieve IATA code via API call'''
        parameters = {
            "term" : name
        }
        headers = {
            "apikey": IATA_KEY
        }
        response = requests.get(url= IATA_API, params= parameters, headers= headers)
        response.raise_for_status()
        data = response.json()

        # Return IATA code
        return data["locations"][0]["code"]
    
    
    def log_search(self, name, IATA, db_path):
        with sqlite3.connect(db_path) as db:
            db.execute("INSERT INTO searches (name, IATA) VALUES (?, ?)", (name, IATA))