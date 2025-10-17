from fastapi import FastAPI

app = FastAPI(title="FastAPI Example App")


@app.get("/")
def root():
    return {"message": "Welcome to AIFlow!"}