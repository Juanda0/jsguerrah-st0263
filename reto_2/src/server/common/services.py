import os
import glob
import datetime
from server import ASSETS_DIR

class FileServices:

    def listFiles(self):
        collection = []
        for filename in os.listdir(ASSETS_DIR):
            file_info = {}
            file_path = os.path.join(ASSETS_DIR, filename)

            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                time = os.path.getmtime(file_path)
                timestamp = datetime.datetime.fromtimestamp(time)
                formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                file_info["name"] = filename
                file_info["size"] = size
                file_info["timestamp"] = formatted_date
                collection.append(file_info)
        print('Respuesra procesada:', collection)
        return collection

    def findFiles(self, search: str) -> list:
        collection = []
        for filename in glob.glob(f"{ASSETS_DIR}/{search}"):
            file_info = {}

            size = os.path.getsize(filename)
            time = os.path.getmtime(filename)
            timestamp = datetime.datetime.fromtimestamp(time)
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            file_info["name"] = os.path.basename(filename)
            file_info["size"] = size
            file_info["timestamp"] = formatted_date
            collection.append(file_info)
        return collection

Service = FileServices()
