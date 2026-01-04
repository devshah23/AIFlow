import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from app.models import *
load_dotenv()
DB_URL=os.getenv("DATABASE_URL","")


engine=create_async_engine(DB_URL)

async_session = async_sessionmaker(engine,expire_on_commit=False)

metadata=SQLModel.metadata
