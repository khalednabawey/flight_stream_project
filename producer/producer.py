from kafka import KafkaProducer
from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import json
import time
import threading
from requests.auth import HTTPBasicAuth
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Update environment variable names
OPENSKY_USERNAME = os.getenv('OPENSKY_USERNAME')
OPENSKY_PASSWORD = os.getenv('OPENSKY_PASSWORD')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def create_kafka_producer(retries=5, retry_delay=5):
    for i in range(retries):
        try:
            return KafkaProducer(
                bootstrap_servers='localhost:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(2, 5, 0)
            )
        except NoBrokersAvailable:
            if i < retries - 1:
                print(
                    f"Kafka not available. Retrying in {retry_delay} seconds... ({i+1}/{retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(
                    "Failed to connect to Kafka after several retries.")


producer = create_kafka_producer()


def produce_data():
    API_URL = "https://opensky-network.org/api/states/all"
    RATE_LIMIT_DELAY = 10

    while True:
        try:
            print("Fetching flight data...")
            response = requests.get(
                API_URL,
                # auth=HTTPBasicAuth(OPENSKY_USERNAME, OPENSKY_PASSWORD)
            )

            if response.ok:
                data = response.json()
                flights = data.get("states", [])[:10]
                if flights:
                    for flight in flights:
                        message = {
                            "callsign": str(flight[1]).strip() if flight[1] else "UNKNOWN",
                            "origin_country": str(flight[2]) if flight[2] else "UNKNOWN",
                            "altitude": float(flight[7]) if flight[7] else 0.0,
                            "velocity": float(flight[9]) if flight[9] else 0.0,
                            "longitude": float(flight[5]) if flight[5] else 0.0,
                            "latitude": float(flight[6]) if flight[6] else 0.0
                        }
                        print(f"Sending flight data: {message}")
                        producer.send("realtime-flights", message)
                        producer.flush()  # Ensure message is sent
                        socketio.emit('producer_message', message)
                else:
                    print("No flight data available")
            else:
                print(f"API Error: {response.status_code} - {response.reason}")
                if response.status_code == 401:
                    print(
                        "Authentication failed. Please check your OpenSky credentials.")

            print(f"Waiting {RATE_LIMIT_DELAY} seconds before next request...")
            time.sleep(RATE_LIMIT_DELAY)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(RATE_LIMIT_DELAY)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(RATE_LIMIT_DELAY)


@app.route('/')
def index():
    return render_template('monitor.html')


if __name__ == '__main__':
    thread = threading.Thread(target=produce_data)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5002)
