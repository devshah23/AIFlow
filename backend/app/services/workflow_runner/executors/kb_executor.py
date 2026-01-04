
import os
from app.embeddings.embedding_service.gemini_embedding import GeminiEmbeddingService
from app.embeddings.vector_store import SupabaseVectorStore
from app.exceptions.Exceptions import InvalidNodeConfigException
from app.services.workflow_runner.executors.base_executor import NodeExecutor
from app.services.workflow_runner.executors.executor_util import ExecutorUtil


class KBExecutor(NodeExecutor):
    async def execute(self, context,upstream_nodes) -> dict:
        try:
            cfg=self.node.config
            if cfg.get("metadata_id",0)==0:
                raise InvalidNodeConfigException("Metadata Id not found for Knowledge Base node.")
            
            upstream_nodes_data = ExecutorUtil.get_data_from_upstream(context, upstream_nodes)
            query="".join(upstream_nodes_data)
            embedding_service=GeminiEmbeddingService(os.environ.get("EMBEDDING_KEY_GEMINI",""))
            query_embedding=await embedding_service.embed_text(query)
            
            if not query_embedding:
                raise Exception("Failed to generate embedding for the query.")
            
            
            vector_store=SupabaseVectorStore()
            output=await vector_store.search_vectors(query_embedding.values or [],cfg.get("metadata_id",0))
            
            if output.get("success") is not True:
                raise Exception(f"Vector store search failed")
            
            return {
                "output":output["results"]
            }   
        except Exception as e:
            raise Exception(f"KB Node Executor failed") from e
        
