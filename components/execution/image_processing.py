import cv2
import numpy as np
from utils.Storage import s3_storage,disk_storage
from utils.Database.database import RedisDatabase
from dotenv import load_dotenv
import os
import json
import pika
import sys
from utils.helpers import np_array_to_BytesIO_stream

load_dotenv()

database=RedisDatabase(os.getenv("REDIS_HOST"),os.getenv("REDIS_PORT"))
storage = s3_storage.S3StorageManager(os.environ.get("AWS_BUCKET_NAME"))
storage=disk_storage.DiskStorage(os.getenv("SHARED_STORAGE_PATH"))

def main():
    print("Worker starting")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST"),port=os.environ.get("RABBITMQ_PORT")))
    channel = connection.channel()
    channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE_NAME"))
    print("Worker is Ready")
    def callback(ch, method, properties, body):
        body = json.loads(body)
        database.update_dict(body["task_id"], {"status": "processing"})

        Processed_Image = process_image(cv2.imdecode(storage.load_to_memory(body["access_means"]), cv2.IMREAD_COLOR), body["operation"])
        if (
            Processed_Image is None
            or Processed_Image.shape[0] == 0
            or Processed_Image.shape[1] == 0
        ):
            print("Error: Image processing failed or Produced an Invalid Result.")
            return None
        image_stream=np_array_to_BytesIO_stream(Processed_Image,body['extension'])
        output_means=storage.save(image_stream,f"{body['task_id']}.{body['extension']}",path="outputs")
        database.update_dict(body["task_id"], {"status": "completed","output_means":output_means}) 
        #TODO: output_means?
        print("finished")
        return True

    channel.basic_consume(queue=os.getenv("RABBITMQ_QUEUE_NAME"), on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def process_image(image: np.ndarray, operation: str):
    if image is None:
        print("Error: Unable to load the image.")
        return None
    # Perform Specified Operation
    if operation == "grayscale":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == "edge_detection":
        result = cv2.Canny(image, 100, 200)
    elif operation == "thresholding":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    elif operation == "inversion":
        result = cv2.bitwise_not(image)
    elif operation == "blurring":
        result = cv2.GaussianBlur(image, (21, 21), 0)
    elif operation == "sharpening":
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        result = cv2.filter2D(image, -1, kernel)
    elif operation == "smoothing":
        result = cv2.medianBlur(image, 5)
    elif operation == "dilation":
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.dilate(image, kernel, iterations=1)
    elif operation == "erosion":
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.erode(image, kernel, iterations=1)
    elif operation == "convert_RGB":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        print("Invalid Operation")
        return

    return result


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
