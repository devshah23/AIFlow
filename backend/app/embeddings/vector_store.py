import os
from postgrest import CountMethod
from supabase import create_client

class SupabaseVectorStore():
    def __init__(self):
        self.client = create_client(os.getenv("SUPABASE_URL",""), os.getenv("SUPABASE_SERVICE_ROLE_KEY",""))

    async def save_vectors(self,data:list):
        try:
            response = self.client.table("embeddings").upsert(data).execute()

            return {
                "success": True,
                "message": "Embeddings upserted successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error upserting embeddings",
            }

    
    async def search_vectors(self,query_vector:list[float],metadata_id:int,top_k:int=5):
        try:
            response = (
                self.client.rpc(
                    "match_vectors_by_meta_id",
                    {
                        "query_vector": query_vector,
                        "match_count": top_k,
                        "filter_metadata_id": metadata_id
                    }
                ).execute()
            )
            data = getattr(response, "data", None)
            if data is None:
                records = []
            elif isinstance(data, list):
                records = data
            else:
                records = [data]

            results_str = "\n\n".join([str(record.get("text")) for record in records])

            return {
                "success": True,
                "results": results_str,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching embeddings",
            }
    async def delete_embeddings_by_metadata_ids(self, metadata_ids: list[int]):
        try:
            response = (
                self.client
                .table("embeddings")
                .delete(count=CountMethod.exact)
                .in_("metadata_id", metadata_ids)
                .execute()
                )
            return True
        except Exception as e:
            raise Exception(f"Error deleting embeddings")
    
    
    