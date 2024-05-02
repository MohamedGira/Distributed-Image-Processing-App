from flask_socketio import SocketIO, emit
from flask import send_file
from utils.Database.database import RedisDatabase
import os
import time

socketio = SocketIO(ping_timeout=30, ping_interval=5)
database=RedisDatabase(os.getenv("REDIS_HOST"),os.getenv("REDIS_PORT"))


@socketio.on("connect")
def test_connect():
    print("Client connected")


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@socketio.on("status")
def status(task_id):
    timeout=60
    poll_interval=5
    for i in range(timeout/poll_interval):
        if task_id is None:
            emit("result", {"status": "Task ID not provided"})
            return
        try:
            response=database.get_dict(task_id)
            if response is None:
                emit("result", {"status": "Task not found"})
            elif response["status"] == "completed":
                emit("result", response)
                return
            else:
                emit("result", response)
            import eventlet
            eventlet.sleep(0)
            time.sleep(poll_interval)
        except Exception as e:
            emit("result", {"status": str(e)})
    emit("timeout", {"task_id":task_id})

        