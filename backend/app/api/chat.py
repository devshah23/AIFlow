from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.chat_response_adapter import ChatResponseAdapter
from app.dependencies.database import get_session
from app.dependencies.services import get_chat_service
from app.exceptions.Exceptions import NotFoundError, ValidationError
from app.models.apis.request import CreateChatRequest
from app.models.apis.response import ApiResponse
from app.models.chats import ChatsCreate
from app.services import chat_service


router=APIRouter(
    prefix="/chat",
)

@router.post("/create")
async def create_chat(req: CreateChatRequest, db:AsyncSession=Depends(get_session),chat_service:chat_service.ChatService=Depends(get_chat_service)):
    try:
        chat=ChatsCreate(name=req.name,workflow_id=req.workflowId,description=req.description)
        response=await chat_service.create_chat(db,chat)
        return ApiResponse(success=True,data=response)
    
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
        response=await chat_service.get_all_chats(db)
        return ApiResponse(success=True,data=response)
    
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
        message_details=ChatResponseAdapter.to_frontend_messages_with_pagination(data.get("message_details",[]))
        data["messageDetails"]=message_details
        data.pop("message_details",None)
        chat=ChatResponseAdapter.to_frontend_chats([data.get("chat",{})])[0]
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
        response=await chat_service.process_workflow_request(db,chat_id,message)
        data={"userMessage":response.get("user_message"),"workflowMessage":response.get("workflow_message")}
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

