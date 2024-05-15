from fastapi import FastAPI, File, UploadFile, Form, HTTPException, WebSocket
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from utils.Storage import s3_storage, disk_storage
from utils.Submitter import rabbitmq_submitter
from utils.Database.database import RedisDatabase
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
import time
import asyncio
import json
from io import BytesIO
from starlette.background import BackgroundTasks
import gc
app = FastAPI()

# Load environment variables
load_dotenv()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Set to desired origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
storage = disk_storage.DiskStorage(os.getenv("SHARED_STORAGE_PATH"))
single_submitter = rabbitmq_submitter.RabbitMQSubmitter(os.getenv("RABBITMQ_HOST"),os.getenv("RABBITMQ_QUEUE_NAME"),os.getenv("RABBITMQ_PORT"))
mpi_submitter = rabbitmq_submitter.RabbitMQSubmitter(os.getenv("RABBITMQ_HOST"),os.getenv("RABBITMQ_MPI_QUEUE_NAME"),os.getenv("RABBITMQ_PORT"))
database = RedisDatabase(os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"))

@app.get("/")
def upload():
    return HTMLResponse(content=open("templates/index.html").read(), status_code=200)


@app.get("/upload")
def upload():
    return HTMLResponse(content=open("templates/index.html").read(), status_code=200)


@app.post("/uploadOne")
async def upload_one(image: UploadFile = File(...), process: str = Form(...)):
    task_id = str(uuid.uuid4())
    extension = image.content_type.split("/")[1] if "/" in image.content_type else "png"

    # Read image stream
    stream = await image.read()
    # Upload image to storage
    response = storage.save(BytesIO(stream), f"{task_id}.{extension}", path="inputs")

    if response is None:
        raise HTTPException(status_code=400, detail="Error uploading image")

    queue_request = {
        "task_id": task_id,
        "operation": process,
        "access_means": response,
        "status": "pending",
        "extension": extension,
        "last_updated": str(datetime.now()),
    }
    database.save_dict(task_id,queue_request)
    size=len(stream)/1024**2
    if size>=5: # use mpi for images > 5mb (network/performance threshold)
        print("submitting to mpi, image size:",size,"MB")
        mpi_submitter.submit(queue_request)
    else:
        print("submitting to single slave, image size:",size,"MB")
        single_submitter.submit(queue_request)
        
    return queue_request

def remove_file(path: str) -> None:
    gc.collect()
    os.unlink(path)

@app.get("/result")
async def result(path: str,background_tasks:BackgroundTasks):
    try:
        background_tasks.add_task(remove_file, path)
        background_tasks.add_task(remove_file, path.replace("/outputs/","/inputs/"))
        return FileResponse(path, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def topicize(topic, message):
    return json.dumps({"message": message, "topic": topic})





# WebSocket connection handler

@app.websocket("/result/{task_id}")
async def status(websocket: WebSocket, task_id):
    await websocket.accept()
    timeout = 60
    poll_interval = 5
    try:
        for i in range(timeout // poll_interval):
            if task_id is None:
                await websocket.send_json(
                    topicize(topic="result", message={"status": "Task ID not provided"})
                )
                return
            response = database.get_dict(task_id)
            if response is None:
                await websocket.send_json(
                    topicize(topic="result", message={"status": "Task ID not found"})
                )
            elif response["status"] in ["success","failed"]:
                await websocket.send_json(topicize(topic="result", message=response))
                return
            else:
                await websocket.send_json(topicize(topic="result", message=response))
            await asyncio.sleep(5)

        await websocket.send_json(
            topicize(topic="result", message={"task_id": task_id, "status": "timeout"})
        )
        await websocket.close(1000)
        return
    except Exception as e:
        print(e)
        import traceback

        traceback.print_exc()
        return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
