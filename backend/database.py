import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializar el cliente de mondoDB
client = AsyncIOMotorClient(MONGODB_URL)

#Seleccionar la base de datos (se creará automaticamente si no existe)
database = client.data_base

#Seleccionar la coleccion (si no existe, se creara automaticamente)
collection = database.mi_coleccion

#Funcion para probar la conexion a la base de datos
async def test_connection():
    try: 
        #1. Verificar la conexion al servidor de MongoDB
        await client.admin.command("ping")
        print("Conexión a MongoDB exitosa")

        #2. Crear un dato de prueba
        doctest = {
            "nombre": "Anderson",
            "edad": 25,
            "ciudad": "Bogotá" 
        }

        #3. Guardar el documento de la conexion 
        print("Guardando documento de prueba en la conexión...")
        result = await collection.insert_one(doctest)
        print(f"Documento guardado con ID: {result.inserted_id}")

        #4 Buscar el dato guardado en la coleccion
        datarequest = await collection.find_one({"_id": result.inserted_id})
        print(f"Documento encontrado: {datarequest}")





    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    #Ejecutar la prueba de conexion
    asyncio.run(test_connection())
            