import os
import uuid
from fastapi import UploadFile
from sqlmodel import select
from supabase import create_client
from app.exceptions.Exceptions import InvalidFileFormatException
from app.models.file_metadata import FileMetadata
from app.models.workflow_nodes import WorkflowNodes, WorkflowNodesTypes
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile
import uuid

class KBFile:
    VALID_FILE_TYPES = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/csv",
            "application/csv",
            "text/plain",
        ]
    def __init__(self, file: UploadFile):
        self.file = file

    def validate_file(self) -> None:
        if self.file.content_type not in self.VALID_FILE_TYPES:
            raise InvalidFileFormatException(
                f"Unsupported file type: {self.file.content_type}"
            )

    def get_file_name(self) -> str:
        file_extension = "dat"
        if self.file.filename:
            file_extension = self.file.filename.rsplit(".", 1)[-1]
        return f"{uuid.uuid4()}.{file_extension}"

    async def get_file_bytes(self) -> bytes:
        file_bytes = await self.file.read()
        if not file_bytes:
            raise Exception("Uploaded file is empty or cannot be read.")
        return file_bytes
    
    def get_content_type(self) -> str:
        return self.file.content_type or ""


class SupabaseService:
    FILE_BUCKET_NAME = "workflow_kb_files"
    FILE_METADATA_TABLE = "file_metadata"
    def __init__(self):
            self.supabase = create_client(os.environ["SUPABASE_URL"],os.environ["SUPABASE_SERVICE_ROLE_KEY"]) 
    
    def __upload_to_storage(self, file_name:str, file_bytes:bytes) -> None:
        upload_res = self.supabase.storage.from_(self.FILE_BUCKET_NAME).upload(
        file_name, file_bytes
        )
        
        # Error without details
        if upload_res is None:
            raise Exception("Supabase file upload error")

        # Error with details in dict
        if isinstance(upload_res, dict) and upload_res.get("error"):
            raise Exception("Supabase File Upload Error:" + upload_res["error"]["message"])
    
    
    def __insert_metadata(self, file_name:str, content_type:str) -> dict:
        insert_res = self.supabase.table(self.FILE_METADATA_TABLE).insert(
                {
                    "file_name": file_name,
                    "file_type": content_type,
                }).execute()
        
        if getattr(insert_res, "error", None):
            raise Exception("Supabase metadata insert error")
        
        insert_data_response = getattr(insert_res, "data", None)
        if not insert_data_response or not isinstance(insert_data_response, list):
            raise Exception("Supabase Insert Error")
        
        return insert_data_response[0]

    def process_file_upload(self,file_name:str, file_bytes:bytes, content_type:str) -> dict:
        self.__upload_to_storage(file_name, file_bytes)
        try:
            return self.__insert_metadata(file_name, content_type)
        except Exception as e:
            # Cleanup orphaned file
            self.supabase.storage.from_(self.FILE_BUCKET_NAME).remove([file_name])
            raise e 


async def upload_file(uploaded_file: UploadFile):
    try:
        file=KBFile(uploaded_file)
        
        file.validate_file()
        file_name = file.get_file_name()
        file_bytes=await file.get_file_bytes()
        
        supabase_instance=SupabaseService()
        uploaded_file_metadata = supabase_instance.process_file_upload(file_name, file_bytes, file.get_content_type())

        return {
            "metadata_id": uploaded_file_metadata.get("id"),
            "success": True,
            "file_name": file_name,
            "file_type": file.get_content_type(),
        }
    
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")


async def get_uploaded_file_metadata(db:AsyncSession,nodes:list[WorkflowNodes]) ->list[WorkflowNodes]:
    try:
        kb_nodes = [node for node in nodes if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE]
        if not kb_nodes:
            return nodes
        metadata_ids = [int(node.config.get("metadata_id", 0)) for node in kb_nodes if node.config.get("metadata_id")]
        if not metadata_ids:
            return nodes
        result = await db.execute(
            select(FileMetadata).where(FileMetadata.id.in_(metadata_ids))
        )
        metadata_records = result.scalars().all()
        metadata_dict = {record.id: record.model_dump() for record in metadata_records}
        
        for node in nodes:
            if node.type == WorkflowNodesTypes.KNOWLEDGEBASENODE and int(node.config.get("metadata_id", 0)) in metadata_dict:
                metadata_obj=metadata_dict[int(node.config.get("metadata_id", 0))]
                fileobj={
                    "metadata_id": int(metadata_obj.get("id",0)),
                    "fileName": metadata_obj.get("file_name"),
                }
                node.config = fileobj
        return nodes
    except Exception as e:
        raise Exception(f"Error retrieving file metadata")

