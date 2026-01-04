from abc import ABC, abstractmethod


class NodeConverter(ABC):
    @abstractmethod
    def convert(self, node: dict):
        pass