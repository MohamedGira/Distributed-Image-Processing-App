from flask import Flask, request
from flask_cors import CORS

import os
import uuid
from Storage import s3_storage
from datetime import datetime
from Submitter import rabbitmq_submitter
from dotenv import load_dotenv

##aws client config

load_dotenv()

storage = s3_storage.S3StorageManager(os.getenv("AWS_BUCKET_NAME"))
submitter=rabbitmq_submitter.RabbitMQSubmitter(os.getenv("RABBITMQ_HOST"),os.getenv("RABBITMQ_QUEUE_NAME"),os.getenv("RABBITMQ_PORT"))
app = Flask(__name__)
CORS(app, origins=["*"])  # set to only react servers later
@app.route("/upload", methods=["POST"])
def upload():
    if "images" not in request.files or "process" not in request.form:
        return f"Missing images or text field,{request.form} ", 400
    # Get the list of images from the POST request
    images = request.files.getlist("images")

    # Get the text from the POST request
    operation = request.form["process"]
    task_ids = []
    queue_requests = []
    for image in images:
        task_id = str(uuid.uuid4())
        # upload image to s3
        response = storage.save(image, task_id, path="inputs")
        if response is None:
            task_ids.append(00)
        else:
            queue_request = {
                "task_id": task_id,
                "operation": operation,
                "access_means": response,
                "status": "pending",
                "last_updated": f"{datetime.now()}",
            }
            queue_requests.append(queue_request)
            task_ids.append(task_id)
    #option, submit immediatly
    for queue_request in queue_requests:
        submitter.submit(queue_request)

    return "Images and text received successfully", 200


if __name__ == "__main__":
    app.run(port=8000)

    