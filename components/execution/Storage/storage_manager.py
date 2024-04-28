from werkzeug.datastructures import FileStorage
class StorageManeger:
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def save(self, file:FileStorage,name,**kwargs):
        """saves image and return access means"""
        pass

    def load(self,access_means):
        """load image from storage"""
        pass