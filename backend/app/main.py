import json
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.workflow import router as workflow_router
from app.api.execution import router as workflow_execution_router
from app.api.chat import router as chat_router
from app.api.upload import file_upload_router 
from fastapi.middleware.cors import CORSMiddleware

from app.utils.exception_handler import register_global_exception_handlers
load_dotenv()

app = FastAPI(title="AIFlow")

origins = [
    "http://localhost:5173",  
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_global_exception_handlers(app)

# Add routers
app.include_router(workflow_router,tags=["Workflow"])
app.include_router(workflow_execution_router,tags=["Workflow Execution"])
app.include_router(file_upload_router,tags=["KB File Upload"])
app.include_router(chat_router,tags=["Chats"])

@app.get("/")
def root():
    return {"message": "Welcome to AIFlow!"}
