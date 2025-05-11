# Real-time Flight Tracking System

A real-time flight tracking system built with Apache Kafka, Python Flask, and OpenSky Network API. The system streams live flight data and visualizes it through an interactive web interface.

## 🛠️ Technologies Used

- Apache Kafka
- Python Flask
- Socket.IO
- OpenSky Network API
- Docker
- Bootstrap

## 🚀 Quick Start

1. **Clone the repository**
   ```powershell
   git clone https://github.com/khalednabawey/flight_stream_project.git
   cd flight_stream_project
   ```

2. **Set up environment variables**
   ```powershell
   # Copy example environment file
   copy .env.example .env
   
   # Edit .env with your OpenSky credentials (optional)
   notepad .env
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start Kafka infrastructure**
   ```powershell
   # Start Kafka and Zookeeper containers
   docker-compose up -d
   
   # Wait 30 seconds for Kafka to initialize
   Start-Sleep -Seconds 30
   ```

5. **Run the applications**
   
   In first terminal:
   ```powershell
   # Start the consumer
   python consumer/consumer.py
   ```
   
   In second terminal:
   ```powershell
   # Start the producer
   python producer/producer.py
   ```

6. **Access the application**
   - Consumer UI: [http://localhost:5001](http://localhost:5001)
   - Producer Monitor: [http://localhost:5002](http://localhost:5002)

## 🏗️ Architecture

```
┌─────────────┐    ┌───────┐    ┌──────────┐    ┌──────────┐
│ OpenSky API │ -> │ Kafka │ -> │ Consumer │ -> │ Web UI   │
└─────────────┘    └───────┘    └──────────┘    └──────────┘
```

- **Producer**: Fetches real-time flight data from OpenSky Network API
- **Kafka**: Handles message queuing and data streaming
- **Consumer**: Processes messages and broadcasts to web clients
- **Web UI**: Real-time visualization of flight data

## 💡 Features

- Real-time flight tracking
- Interactive web interface
- Message queuing with Kafka
- WebSocket real-time updates
- Docker containerization
- Rate limiting handling
- Error recovery

## 🛑 Troubleshooting

1. **Kafka Connection Issues**
   ```powershell
   # Check if containers are running
   docker ps
   
   # Check Kafka logs
   docker logs kafka_project-kafka-1
   ```

2. **Rate Limiting**
   - Anonymous users: 1 request/minute
   - Registered users: Better rate limits
   - Add OpenSky credentials in `.env` file

3. **Port Conflicts**
   - Ensure ports 5001, 5002, 9092, and 2181 are available
   - Check running services:
   ```powershell
   netstat -ano | findstr "5001 5002 9092 2181"
   ```



## ✨ Acknowledgments

- [OpenSky Network](https://opensky-network.org/) for providing the flight data API
- [Apache Kafka](https://kafka.apache.org/) for the streaming platform
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/) for WebSocket support
