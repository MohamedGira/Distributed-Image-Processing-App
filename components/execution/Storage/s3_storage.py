from Storage.storage_manager import StorageManeger
from dotenv import load_dotenv
import os
import boto3
from werkzeug.datastructures import FileStorage
from pathlib import Path

# bytes
import io
import numpy as np
import cv2


class S3StorageManager(StorageManeger):
    def __init__(self, bucket_name):
        self.bucket = bucket_name
        load_dotenv()
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS"),
            aws_secret_access_key=os.environ.get("AWS_SECRET"),
        )

    def save(self, file: FileStorage, name, path=""):
        key = (Path(path).joinpath(name).as_posix(),)
        try:
            self.client.upload_fileobj(
                file,
                self.bucket,
                Path(path).joinpath(name).as_posix(),
                ExtraArgs={"ContentType": file.content_type},
            )
            return key
        except Exception as e:
            print("Something Happened: ", e)

    def load(self, access_means):
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=access_means)
            return response["Body"]
        except Exception as e:
            print("Something Happened: ", e)

    def load_to_memory(self, access_means) -> np.ndarray:
        try:
            file_stream = io.BytesIO()
            self.client.download_fileobj(self.bucket, access_means, file_stream)
            file_stream.seek(0)
            file_bytes = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            return img

        except Exception as e:
            print("Something Happened: ", e)
