from utils.Storage.storage_manager import StorageManeger
from pathlib import Path
from werkzeug.datastructures import FileStorage
import numpy as np
from io import BytesIO
import traceback

class DiskStorage(StorageManeger):
    def __init__(self, storage_path):
        super().__init__(storage_path)

    def save(self, stream: BytesIO, name, path=""):
        """saves image and return access means"""
        access_means = Path(self.storage_path).joinpath(path, name).as_posix()
        with open(access_means, "wb") as f:
            f.write(stream.getvalue())
        return access_means

    def load_to_memory(self, access_means) -> np.ndarray:
        try:
            with open(access_means, "rb") as file:
                file_bytes = np.frombuffer(file.read(), dtype=np.uint8)
                return file_bytes
        except Exception as e:
            print("Something Happened: ", e)
            traceback.print_exc()
