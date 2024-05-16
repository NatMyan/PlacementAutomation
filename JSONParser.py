from Parser11 import Parser11

import json


class JSONParser(Parser11):
    def __init__(self):
        self._data = {}

    def parse_input_file(self, lines):
        if lines:
            json_content = "\n".join(lines)
            try:
                self._data = json.loads(json_content)
            except json.JSONDecodeError:
                self._data = {}

    def get_data(self):
        return self._data
