from flask import Flask
import mysql.connector
import json

app = Flask(__name__)

config = {
        'user': 'root',
        'password': 'your_password',
        'host': 'db',
        'port': '3306',
        'database': 'your_database',
    }

query = (
    "SELECT elr_code, mileage_from, mileage_to, "
    "LAG (mileage_to, 1, null) OVER (PARTITION BY elr_code ORDER BY mileage_from ASC) AS previous_end "
    "FROM mileages"
)

def get_elrs(config, query):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)
    results = [{"elr_code": elr_code, "mileage_from": mileage_from, "mileage_to": mileage_to, "previous_end": previous_end} for (elr_code, mileage_from, mileage_to, previous_end) in cursor]
    cursor.close()
    connection.close()
    return results


@app.route('/')
def index() -> str:
    return "running"

@app.route('/elrs')
def elrs() -> str:
    return json.dumps(get_elrs(config=config, query=query))

if __name__ == '__main__':
    app.run(host='0.0.0.0')