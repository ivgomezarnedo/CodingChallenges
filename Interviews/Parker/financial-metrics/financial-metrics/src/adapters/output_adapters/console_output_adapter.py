from interfaces.output_interface import OutputInterface
import json

class ConsoleOutputAdapter(OutputInterface):

    def output_data(self, data):
        print(json.dumps(data, indent=2))
