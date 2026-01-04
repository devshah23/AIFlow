from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

def register_global_exception_handlers(app: FastAPI):
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        # Log full stack trace
        logger.error(f"SQLAlchemy error: {exc}", exc_info=True)
        if isinstance(exc, IntegrityError):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Database integrity error."},
            )
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Database error occurred."},
        )

    # Handle Pydantic validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": "Validation error", "errors": exc.errors()},
        )

    # Handle HTTP exceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        exc_message= str(exc.detail)
        if len(exc_message)>60:
            exc_message=exc_message[:57]+"..."
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc_message},
        )

    # Catch-all for unexpected exceptions
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error."},
        )
