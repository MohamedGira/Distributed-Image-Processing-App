from flask import Flask, render_template, request
from flask_cors import CORS

import os
import uuid
from utils.Storage import s3_storage,disk_storage
from datetime import datetime
from utils.Submitter import rabbitmq_submitter
from utils.Database.database import RedisDatabase
from dotenv import load_dotenv
from io import BytesIO

##aws client config

load_dotenv()

storage=disk_storage.DiskStorage(os.getenv("SHARED_STORAGE_PATH"))
storage = s3_storage.S3StorageManager(os.getenv("AWS_BUCKET_NAME"))
submitter=rabbitmq_submitter.RabbitMQSubmitter(os.getenv("RABBITMQ_HOST"),os.getenv("RABBITMQ_QUEUE_NAME"),os.getenv("RABBITMQ_PORT"))
database=RedisDatabase(os.getenv("REDIS_HOST"),os.getenv("REDIS_PORT"))

app = Flask(__name__)
CORS(app, origins=[""])  #TODO: set to desired later

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == "GET":
        return render_template('index.html')

    if "images" not in request.files or "process" not in request.form:
        return f"Missing images or text field,{request.form} ", 400
    # Get the list of images from the POST request
    images = request.files.getlist("images")
    print(request.files)
    print(request.files.getlist("images"))
    # Get the text from the POST request
    operation = request.form["process"]
    task_ids = []
    queue_requests = []
    for image in images:
        task_id = str(uuid.uuid4())
        extension=image.content_type.split('/')[1] if len(image.content_type.split('/'))>1 else "png"
        # upload image to s3
        stream=image.read()
        response = storage.save(BytesIO(stream), f"{task_id}.{extension}", path="inputs")
        if response is None:
            task_ids.append(00)
        else:
            queue_request = {
                "task_id": task_id,
                "operation": operation,
                "access_means": response,
                "status": "pending",
                "extension":extension,
                "last_updated": f"{datetime.now()}",
            }
            queue_requests.append(queue_request)
            task_ids.append(task_id)
    #option, submit immediatly
    for queue_request in queue_requests:
        database.save_dict(task_id,queue_request)
        submitter.submit(queue_request)
        

    return "Images and text received successfully", 200


#TODO: 0 auth, 0 denial of service protection... but meh
@app.route("/status/<task_id>", methods=["GET"])
def status(task_id):
    if task_id is None:
        return "Task ID not provided", 400
    response=database.get_dict(task_id)
    return {"status":response.get("status"),}, 200
    # Get the status of the task from the database
    status = "pending"
    return status, 200

if __name__ == "__main__":
    app.run(port=8000,debug=True)

    

