from kafka import KafkaConsumer
from flask_socketio import SocketIO, emit
from flask import Flask
import json
import threading
import time
import kafka.errors
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def consume():
    while True:
        try:
            print("Attempting to connect to Kafka...")
            consumer = KafkaConsumer(
                'realtime-flights',
                bootstrap_servers=['localhost:9092'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                group_id='flight_consumer_group',
                security_protocol='PLAINTEXT',
                api_version=(2, 5, 0),
                retry_backoff_ms=1000,
                consumer_timeout_ms=1000
            )

            print("Connected to Kafka broker")
            while True:
                try:
                    for msg in consumer:
                        if msg.value:
                            print("\n=== Received Flight Data ===")
                            print(f"Topic: {msg.topic}")
                            print(f"Partition: {msg.partition}")
                            print(f"Offset: {msg.offset}")
                            print(f"Data: {json.dumps(msg.value, indent=2)}")
                            print("==========================\n")
                            socketio.emit('flight_data', msg.value)
                except kafka.errors.KafkaTimeoutError:
                    print(".", end="", flush=True)  # Show activity
                    continue

        except kafka.errors.NoBrokersAvailable:
            print("No brokers available. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(5)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    thread = threading.Thread(target=consume)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5001)
