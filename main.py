from fastapi import FastAPI

from models import base
from db.db import engine

from routes.user import router as user_router
from routes.book import router as book_router
from routes.auth import router as auth_router

base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Review API",
    description="A simple Book Review API built with FastAPI.",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(auth_router)

@app.get("/test")
def test():
    return {"test":"working"}