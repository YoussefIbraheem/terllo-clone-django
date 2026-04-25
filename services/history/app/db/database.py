from app.core.config import settings
from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.models.event import Event


async def connect_to_mongo():
    client = AsyncMongoClient(host=settings.MONGO_DB_URL)
    database = client[settings.MONGO_DB_NAME]
    print(f"connecting to {settings.MONGO_DB_NAME}")
    await init_beanie(database=database,document_models=[Event])
    print("MongoDB connection established")
    
    
async def close_mongo():
    
    client = AsyncMongoClient(settings.MONGO_DB_URL)
    print("Closing MongoDB connection...")
    await client.close()
    print("MongoDB connection closed")