from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def processInput(self, event):
        pass