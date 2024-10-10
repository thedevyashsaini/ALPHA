import psycopg2
import json

# Load database credentials from db.json file
with open('db.json') as f:
    credentials = json.load(f)

def connect():
    # Connect to the ElephantSQL database
    conn = psycopg2.connect(
        database=credentials["name"],
        user=credentials["user"],
        password=credentials["passw"],
        host=credentials["host"],
        port=credentials["port"]
    )
    return conn