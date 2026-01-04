
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.models.workflows import Workflows
from app.repositories.base import BaseRepository
from app.exceptions.Exceptions import DatabaseError, NotFoundError
from sqlalchemy.exc import SQLAlchemyError


class WorkflowRepository(BaseRepository[Workflows]):
    def __init__(self):
        super().__init__(Workflows)
    
    async def get_entire_workflow(self, db: AsyncSession, id: int) -> Workflows:
        try:
            stmt = (
                select(Workflows)
                .options(
                    selectinload(Workflows.nodes),
                    selectinload(Workflows.edges),
                )
                .where(Workflows.id == id)
            )

            result = await db.scalars(stmt)
            workflow = result.first()

            if not workflow:
                raise NotFoundError(f"Workflow with id {id} not found")

            return workflow

        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch entire workflow") from e
    

    async def get_all(self, db: AsyncSession) -> list[Workflows]:
        try:
            stmt = select(Workflows)
            result = await db.scalars(stmt)
            return list(result.all())

        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch workflow list") from e
