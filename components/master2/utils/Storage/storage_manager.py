from werkzeug.datastructures import FileStorage
from numpy import ndarray
from io import BytesIO
class StorageManeger:
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def save(self, file:BytesIO,name,**kwargs):
        """saves image and return access means"""
        pass

    def load(self,access_means):
        """load image from storage"""
        pass   
    def load_to_memory(self, access_means) -> ndarray:
        pass
