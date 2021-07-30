from abc import ABC, abstractmethod

class Snapshot(ABC):

    @abstractmethod
    def evaluate_difference(self):
        raise NotImplementedError