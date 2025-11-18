import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from app.models import *
load_dotenv()
DB_URL=os.getenv("DATABASE_URL","")


engine=create_async_engine(DB_URL)

async_session = async_sessionmaker(engine,expire_on_commit=False)

metadata=SQLModel.metadata


async def get_session():
    async with async_session() as session:
        yield session