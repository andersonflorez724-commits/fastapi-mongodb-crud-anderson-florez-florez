import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)

database = client.tienda_db
productos_collection = database.get_collection("productos")
pedidos_collection = database.get_collection("pedidos")