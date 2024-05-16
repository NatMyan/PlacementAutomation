from abc import ABC, abstractmethod

class Parser11(ABC):
    @abstractmethod
    def parse_input_file(self, lines):
        pass
    