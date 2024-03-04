from interfaces.input_interface import InputInterface
import json

class JSONInputAdapter(InputInterface):

    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_data(self, id: str):
        # In a real application, it would be searched for data by id.
        with open(self.file_path) as file:
            data = json.load(file)
            return data