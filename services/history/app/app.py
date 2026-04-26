from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.database import connect_to_mongo, close_mongo
from app.apis.event_api import router as event_router
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


app.include_router(event_router)