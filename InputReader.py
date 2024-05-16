class InputReader:
    def __init__(self, file_name):
        self._file_name = file_name

    def read_input(self):
        try:
            with open(self._file_name, 'r') as file:
                return file.readlines()
        except:
            print("File not found")
