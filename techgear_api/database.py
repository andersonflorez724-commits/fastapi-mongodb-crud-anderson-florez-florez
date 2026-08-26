import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB = os.getenv("MONGODB_DB", "techgear_db")
client = AsyncIOMotorClient(MONGODB_URL)

database = client[MONGODB_DB]
productos_collection = database.get_collection("productos")
pedidos_collection = database.get_collection("pedidos")