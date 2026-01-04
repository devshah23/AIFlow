
from fastapi import APIRouter, HTTPException, UploadFile


file_upload_router=APIRouter()

from app.models.apis.response import ApiResponse
from app.services.crud_services.uploads.kb_file_upload import upload_file

@file_upload_router.post("/upload_kb_file")
async def upload_kb_file(file: UploadFile):
    """
    Endpoint to upload a knowledge base file.
    """
    try:
        result = await upload_file(file)
        if result is None:
            raise Exception("File upload failed without a specific error.")
        if result.get("success") is False:
            raise Exception(result.get("error") or "File upload failed.")
        
        
        return ApiResponse(success=True, data={"metadata_id": result.get("metadata_id"),
                                               "file_name": result.get("file_name"),
                                               })
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=str(e) or "Error Uploading File"
        )
        
        
