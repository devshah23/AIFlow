from abc import ABC, abstractmethod

class BaseProvider(ABC):
    def __init__(self, api_key: str, model: str , config: dict,temperature:float ):
        self.api_key = api_key
        self.model = model
        self.client=None
        self.temperature=temperature
        self.config = config or {}

    @abstractmethod
    def create_client(self):
        """Return the provider-specific client"""
        pass

