from fastapi import FastAPI
from .core.config import settings
from contextlib import asynccontextmanager
from .db.database import connect_to_mongo, close_mongo
@asynccontextmanager
async def lifespan(app:FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo()
    



app = FastAPI(lifespan=lifespan)




@app.get("/")
def read_root():
    return {"project_name": settings.PROJECT_NAME}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
