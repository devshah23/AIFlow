from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.convertors.chat_convertor_utils import ChatConvertorUtils
from app.dependencies.database import get_session
from app.dependencies.services import get_chat_service
from app.exceptions.Exceptions import DatabaseError, NotFoundError, ValidationError
from app.models.apis.response import ApiResponse
from app.models.chats import ChatsCreate
from app.services import chat_service


router=APIRouter(
    prefix="/chat",
)

@router.post("/create")
async def create_chat(chat_data: dict, db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        chat_name=chat_data.get("name","")
        chat_workflow_id=int(chat_data.get("workflowId",0))
        chat_description=chat_data.get("description","")
        chat=ChatsCreate(name=chat_name,workflow_id=chat_workflow_id,description=chat_description)
        response=await chat_service.create_chat(db,chat)
        return ApiResponse(success=True,data=ChatConvertorUtils.convert_chat_response_format([response])[0])
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    
    
@router.get("/all")
async def get_all_chats(db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        data=await chat_service.get_all_chats(db)
        return ApiResponse(success=True,data=ChatConvertorUtils.convert_chat_response_format(data))
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    
    
@router.get("/{chat_id}")
async def get_chat(chat_id: int, db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        data=await chat_service.get_chat(db,chat_id)
        message_details=ChatConvertorUtils.convert_messages_response_format(data.get("message_details",[]))
        data["messageDetails"]=message_details
        data.pop("message_details",None)
        chat=ChatConvertorUtils.convert_chat_response_format([data.get("chat",{})])[0]
        data["chat"]=chat
        return ApiResponse(success=True,data=data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/messages/{chat_id}")
async def get_messages(chat_id:int, limit:int=20, cursor:int|None=None, db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        data=await chat_service.get_messages(db,chat_id,limit,cursor)
        data=ChatConvertorUtils.convert_messages_response_format(data)
        return ApiResponse(success=True,data=data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@router.post("/run/{chat_id}")
async def send_message(chat_id: int,message=Body(..., embed=True), db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        response=await chat_service.execute_workflow(db,chat_id,message)
        user_msg=ChatConvertorUtils.convert_message_response_format(response.get("user_message"))
        workflow_msg=ChatConvertorUtils.convert_message_response_format(response.get("workflow_message"))
        data={"userMessage":user_msg,"workflowMessage":workflow_msg}


        return ApiResponse(success=True,data=data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.delete("/delete/{chat_id}")
async def delete_chat(chat_id: int, db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        await chat_service.delete_chat(db,chat_id)
        return ApiResponse(success=True,data={"message": f"Chat {chat_id} deleted"})
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

