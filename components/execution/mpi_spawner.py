#!/usr/bin/python3
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
import subprocess
from pathlib import Path
load_dotenv()
executor_path="/bata/src/cleanCopy/components/execution/execution_mpi.py"
database=RedisDatabase(os.getenv("REDIS_HOST"),os.getenv("REDIS_PORT"))
storage = s3_storage.S3StorageManager(os.environ.get("AWS_BUCKET_NAME"))
storage=disk_storage.DiskStorage(os.getenv("SHARED_STORAGE_PATH"))

def main():
    print("Worker starting")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST"),port=os.environ.get("RABBITMQ_PORT")))
    channel = connection.channel()
    channel.queue_declare(queue=os.getenv("RABBITMQ_MPI_QUEUE_NAME"))
    print("Worker is Ready")
    def callback(ch, method, properties, body):
        with open("/bata/test.log",'w') as output:
            try:
                output.write("revieced")
                print('recieved')
                body = json.loads(body)
                output_name=f"{body['task_id']}.{body['extension']}"
                output_dir="outputs"
                output_full_path=Path(storage.storage_path).joinpath(output_dir, output_name).as_posix()
                cmd=f"mpirun -n 4 --hostfile /bata/src/cleanCopy/components/execution/hostfile\
                    python3 {executor_path} --access_means {body["access_means"]} --output_dir {output_dir} --output_name {output_name}\
                    --shared_storage {os.getenv("SHARED_STORAGE_PATH")} --operation {body["operation"]} --extension {body['extension']}"
                print("rinning",cmd)
                output.write(cmd)
                database.update_dict(body["task_id"], {"status": "processing"})
                process=subprocess.run(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if (process.returncode ==0):
                    database.update_dict(body["task_id"], {"status": "success","output_means":output_full_path}) 
                return not process.returncode
            except Exception as e:
                output.write(str(e))

    channel.basic_consume(queue=os.getenv("RABBITMQ_MPI_QUEUE_NAME"), on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
