from fastapi import FastAPI
from routers import users
from contextlib import AbstractAsyncContextManager
from backend import models

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def health_check():
    return "hello"