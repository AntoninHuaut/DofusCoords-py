import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import scheduled_task
from flask import Flask, jsonify

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', seconds=1)
atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask server!'})

app.run(debug=True, use_reloader=False)