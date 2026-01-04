import os
from app.embeddings.embedding_model import EmbeddingModel
from google import genai
from google.genai.client import AsyncClient
from google.genai import types

class GeminiEmbeddingService(EmbeddingModel):
    client:AsyncClient
    def __init__(self, api_key: str, model: str = "gemini-embedding-001"):
        super().__init__(api_key=api_key, model=model)
        
        self.client = genai.Client(api_key=self.api_key).aio

    async def embed_chunks(self, text: list[str]):
        response=await self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT",output_dimensionality=int(os.environ.get("EMBEDDING_SIZE",256)))
        )
        return response.embeddings
    
    
    async def embed_text(self, text: str):
        response = await self.client.models.embed_content(
            model=self.model,
            contents=[text],
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY",output_dimensionality=int(os.environ.get("EMBEDDING_SIZE",256)))
        )
        
        if response.embeddings:
            return response.embeddings[0]
        return None
        