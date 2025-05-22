import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_socketio import SocketIO

from scheduler import scheduled_task, latest_coordinates

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

previous_coordinates = None


def check_coordinates_change():
    global previous_coordinates
    current_coordinates = latest_coordinates.copy()
    if current_coordinates != previous_coordinates:
        socketio.emit('coordinates_update', current_coordinates)
        previous_coordinates = current_coordinates


scheduler = BackgroundScheduler()
scheduler.add_job(lambda: scheduled_task(check_coordinates_change), 'interval', seconds=0.5)
atexit.register(lambda: scheduler.shutdown())
scheduler.start()


@app.route('/')
def home():
    return jsonify(latest_coordinates)


@socketio.on('connect')
def handle_connect():
    socketio.emit('coordinates_update', latest_coordinates)


app.run(debug=True, use_reloader=False)
