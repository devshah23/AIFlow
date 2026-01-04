import os
import uuid
from fastapi import UploadFile
from sqlmodel import select
from supabase import create_client

from app.exceptions.Exceptions import InvalidFileFormatException
from app.models.file_metadata import FileMetadata
from app.models.workflow_nodes import WorkflowNodes, WorkflowNodesTypes
from sqlalchemy.ext.asyncio import AsyncSession


async def upload_file(file: UploadFile):
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/csv",
        "application/csv",
        "text/plain",
    }

    # --- Validate File Type ---
    if file.content_type not in allowed_types:
        raise InvalidFileFormatException(f"Unsupported file type: {file.content_type}")

    if file.filename:
        ext = file.filename.rsplit(".", 1)[-1]
    else:
        ext = "dat"

    new_name = f"{uuid.uuid4()}.{ext}"

    supabase = create_client(os.environ["SUPABASE_URL"],os.environ["SUPABASE_SERVICE_ROLE_KEY"])

    # --- Read File Content Once ---
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise Exception("Uploaded file is empty.")
    except Exception as e:
        raise Exception(f"Failed to read uploaded file: {str(e)}")

    # --- Upload to Supabase Storage ---
    try:
        upload_res = supabase.storage.from_("workflow_kb_files").upload(
           new_name, file_bytes
        )

        # Supabase Python client sometimes returns None for errors
        if upload_res is None:
            raise Exception("Supabase returned None on file upload.")

        # Sometimes returns dict with 'error'
        if isinstance(upload_res, dict) and upload_res.get("error"):
            raise Exception(upload_res["error"]["message"])
        

    except Exception as e:
        raise Exception(f"Failed to upload file to Supabase storage")

    try:
        insert_res = supabase.table("file_metadata").insert(
                {
                    "file_name": new_name,
                    "file_type": file.content_type,
                }
            ).execute()
        if getattr(insert_res, "error", None):
            raise Exception(f"Supabase insert error")
        
        insert_data_response = getattr(insert_res, "data", None)
        if not insert_data_response or not isinstance(insert_data_response, list):
            raise Exception("Invalid response from Supabase on insert.")
        
        insert_result_data = insert_data_response[0]
    except Exception as e:
        # Cleanup orphaned file
        try:
            supabase.storage.from_("workflow_kb_files").remove([new_name])
        except Exception:
            pass

        raise Exception(f"Failed to store file metadata")

    return {
        "metadata_id": insert_result_data.get("id"),
        "success": True,
        "file_name": new_name,
        "file_type": file.content_type,
    }



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

