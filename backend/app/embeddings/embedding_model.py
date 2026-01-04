
from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client=None
    
    @abstractmethod
    async def embed_chunks(self, chunk: list[str]):
        pass
    
    @abstractmethod
    async def embed_text(self,text:str):
        pass