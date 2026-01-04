import asyncio
import os
from typing import List
from app.embeddings.embedding_service.gemini_embedding import GeminiEmbeddingService
from app.embeddings.vector_store import SupabaseVectorStore
from app.text_extraction.extracter_factory import ExtracterFactory



class EmbeddingOrchestratorService:
    """Runs the entire file processing workflow fully in the background."""

    def __init__(self):
        self.vector_store = SupabaseVectorStore()
        self.embedding_service = GeminiEmbeddingService(os.environ.get("EMBEDDING_KEY_GEMINI",""))

    async def _process_file_task(self, file_type: str, file_path: str, metadata_id: int):
        """Internal method to process file asynchronously."""
        try:
            extractor= ExtracterFactory.get_extracter(file_path,file_type)
            chunks = extractor.extract_text()

            data_to_upsert: List[dict] = []
            embeddings = await self.embedding_service.embed_chunks(chunks)
            if embeddings and len(chunks) != len(embeddings):
                raise ValueError("Mismatch between number of chunks and embeddings generated.")
            
            if not embeddings:
                raise ValueError("No embeddings were generated for the provided chunks.")
            for chunk, vector in zip(chunks, embeddings):
                data_to_upsert.append({
                                "text": chunk,
                                "vector": vector.values,
                                "metadata_id": metadata_id
                            })
            

            response=await self.vector_store.add_vectors(data_to_upsert)
            if response.get("success") is not True:
                raise Exception(f"Failed to add vectors: {response.get('message','Unknown error')}")
            else:
                print(f"[Background] Successfully processed file {file_path} and stored embeddings.")

        except Exception as e:
            print(f"[Background] Error processing file {file_path}: {str(e)}")


    def generate_store_embeddings(self, file_type: str, file_path: str, metadata_id: int,background_tasks):
        def wrapper():
            asyncio.run(self._process_file_task(file_type, file_path, metadata_id))
        
        
        background_tasks.add_task(
            wrapper
        )


    async def delete_embeddings_by_metadata_ids(self, metadata_ids: list[int]):
        if not metadata_ids:
            return True
        res=self.vector_store.client.table("file_metadata").select("file_name").in_("id",metadata_ids).execute()
        self.vector_store.client.storage.from_(os.environ.get("SUPABASE_BUCKET_KB","")).remove(
            [record["file_name"] for record in res.data]
        )
        return await self.vector_store.delete_embeddings_by_metadata_ids(metadata_ids)
    