from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def register_global_exception_handlers(app: FastAPI):
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        if isinstance(exc, IntegrityError):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Constraint violation error."},
            )
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Database error."},
        )

    # Handle Pydantic validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": "Validation error", "errors": exc.errors()},
        )

    # Handle HTTP exceptions
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        exc_message= str(exc.detail)
        if len(exc_message)>20:
            exc_message=exc_message[:20]+"..."
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc_message},
        )

    # Catch-all for unexpected exceptions
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error."},
        )
