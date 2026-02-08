from fastapi import APIRouter, HTTPException, UploadFile
from app.models.apis.response import ApiResponse
from app.services.crud_services.uploads.kb_file_upload import upload_file

file_upload_router=APIRouter()
@file_upload_router.post("/upload_kb_file")
async def upload_kb_file(file: UploadFile):
    """
    Endpoint to upload a knowledge base file.
    """
    try:
        error_message="File upload failed. Please ensure the file is valid and try again."
        
        result = await upload_file(file)
        
        if result is None:
            raise Exception(error_message)
        
        return ApiResponse(success=True, 
                           data={"metadata_id": result.get("metadata_id"),
                                "file_name": result.get("file_name"),
                                }
                           )
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
        
        
