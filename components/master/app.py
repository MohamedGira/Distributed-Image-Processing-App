from flask import Flask, render_template, request,send_file
from flask_cors import CORS

import os
import uuid
from utils.Storage import s3_storage,disk_storage
from datetime import datetime
from utils.Submitter import rabbitmq_submitter
from utils.Database.database import RedisDatabase
from dotenv import load_dotenv
from io import BytesIO
from events import socketio


app = Flask(__name__)
socketio.init_app(app)
##aws client config

load_dotenv()

storage = s3_storage.S3StorageManager(os.getenv("AWS_BUCKET_NAME"))
storage=disk_storage.DiskStorage(os.getenv("SHARED_STORAGE_PATH"))
submitter=rabbitmq_submitter.RabbitMQSubmitter(os.getenv("RABBITMQ_HOST"),os.getenv("RABBITMQ_QUEUE_NAME"),os.getenv("RABBITMQ_PORT"))
database=RedisDatabase(os.getenv("REDIS_HOST"),os.getenv("REDIS_PORT"))


CORS(app, origins=[""])  #TODO: set to desired later

@app.route("/upload", methods=["GET"])
def upload():
    return render_template('index.html')

@app.route("/uploadOne", methods=["POST"])
def uploadOne():
    if "image" not in request.files or "process" not in request.form:
        return f"Missing images or text field,{request.form} ", 400
    #Get the list of images from the POST request
    image = request.files.get("image")
    operation = request.form["process"]
    task_id = str(uuid.uuid4())
    extension=image.content_type.split('/')[1] if len(image.content_type.split('/'))>1 else "png"
    # upload image to s3
    stream=image.read()
    #response = storage.save(BytesIO(stream), f"{task_id}.{extension}", path="inputs")
    response = "mock"
    if response is None:
        return {"message":"Error uploading image"}, 400
    else:
        queue_request = {
            "task_id": task_id,
            "operation": operation,
            "access_means": response,
            "status": "pending",
            "extension":extension,
            "last_updated": f"{datetime.now()}",
        }
        return queue_request, 200

#TODO: for s3, check how image must be returned. loaded then sent?
def retrieve_image(output_means):
    if issubclass(storage,disk_storage.DiskStorage):
        return output_means
    elif issubclass(storage,s3_storage.S3StorageManager):
        return output_means
    else:
        raise NotImplementedError("shouldn't reach here")
    
#TODO: 0 auth, 0 denial of service protection... but meh
@app.route("/result",methods=["GET"])
def result():
    output_means=request.args.get("path")
    if output_means is None:
        return "Missing path", 400
    try:
        return send_file(output_means)
    except Exception as e:
        return str(e), 400




if __name__ == "__main__":
    socketio.run(app,port=8000,debug=True)

    

