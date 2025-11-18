import json
from fastapi import FastAPI, HTTPException,Request
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
load_dotenv()

app = FastAPI(title="AIFlow")

@app.middleware("http")
async def catch_malformed_json(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            await request.json()
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Malformed JSON. Please check your request body.",
                    "errors": {
                        "body": "Invalid JSON format"
                    }
                }
            )
    return await call_next(request)


@app.get("/")
def root():
    return {"message": "Welcome to AIFlow!"}
