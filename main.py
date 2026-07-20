from fastapi import FastAPI
from mangum import Mangum

from models import base
from db.db import engine

from routes.user import router as user_router
from routes.film import router as film_router
from routes.auth import router as auth_router

base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Film Review API",
    description="A simple Film Review API built with FastAPI.",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(film_router)
app.include_router(auth_router)

@app.get("/test")
def test():
    return {"test":"working"}

handler = Mangum(app)