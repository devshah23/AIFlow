
from abc import ABC, abstractmethod
import os
import io

from supabase import Client, create_client


class BaseExtracter(ABC):
    """Base class for text extracters."""
    def __init__(self,file_name: str):
        self.file_name = file_name
    
    @abstractmethod
    def extract_text(self) -> list[str]:
        """Extract text from the file."""
        pass
    
    def get_file_from_storage(self):
        """Retrieve the file from storage."""
        
        supabase_client:Client=create_client(os.environ.get("SUPABASE_URL",""),os.environ.get("SUPABASE_SERVICE_ROLE_KEY",""))
        
        try:
            file_data:bytes=supabase_client.storage.from_(os.environ.get("SUPABASE_BUCKET_KB","")).download(self.file_name)
        except Exception as e:
            raise FileNotFoundError(f"File {self.file_name} not found in storage.") from e
        
        data_stream=io.BytesIO(file_data)
        return data_stream