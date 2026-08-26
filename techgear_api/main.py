from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from typing import List
from database import productos_collection, pedidos_collection
from schemas import (
    ProductoCreate, ProductoResponse, 
    PedidoCreate, PedidoResponse
)

app = FastAPI(title="API REST de Productos y Pedidos")

# Helper para convertir el _id de MongoDB (ObjectId) a string id
def format_doc(doc):
    if doc:
        doc["id"] = str(doc["_id"])
    return doc

@app.get("/")
def inicio():
    return {"mensaje": "API REST corriendo correctamente"}

# ==================== ENDPOINTS PRODUCTOS ====================

@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    nuevo = await productos_collection.insert_one(producto.model_dump())
    creado = await productos_collection.find_one({"_id": nuevo.inserted_id})
    return format_doc(creado)

@app.get("/productos", response_model=List[ProductoResponse])
async def obtener_productos():
    productos = []
    async for doc in productos_collection.find():
        productos.append(format_doc(doc))
    return productos

@app.get("/productos/{producto_id}", response_model=ProductoResponse)
async def obtener_producto_por_id(producto_id: str):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=400, detail="ID no válido")
    doc = await productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return format_doc(doc)

# ==================== ENDPOINTS PEDIDOS ====================

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pedido(pedido: PedidoCreate):
    # Validar stock y descontar de cada producto
    for item in pedido.productos:
        if not ObjectId.is_valid(item.producto_id):
            raise HTTPException(status_code=400, detail=f"ID de producto no válido: {item.producto_id}")

        producto = await productos_collection.find_one({"_id": ObjectId(item.producto_id)})
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")

        if producto["stock"] < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{producto["nombre"]}'. Disponible: {producto["stock"]}, solicitado: {item.cantidad}",
            )

        await productos_collection.update_one(
            {"_id": ObjectId(item.producto_id)},
            {"$inc": {"stock": -item.cantidad}},
        )

    nuevo = await pedidos_collection.insert_one(pedido.model_dump())
    creado = await pedidos_collection.find_one({"_id": nuevo.inserted_id})
    return format_doc(creado)

@app.get("/pedidos", response_model=List[PedidoResponse])
async def obtener_pedidos():
    pedidos = []
    async for doc in pedidos_collection.find():
        pedidos.append(format_doc(doc))
    return pedidos

@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
async def obtener_pedido_por_id(pedido_id: str):
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(status_code=400, detail="ID no válido")
    doc = await pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return format_doc(doc)

@app.put("/productos/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(producto_id: str, producto: ProductoCreate):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)}, 
        {"$set": producto.model_dump()}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    doc = await productos_collection.find_one({"_id": ObjectId(producto_id)})
    return format_doc(doc)

@app.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: str):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=400, detail="ID no válido")
        
    resultado = await productos_collection.delete_one({"_id": ObjectId(producto_id)})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    return {"mensaje": "Producto eliminado exitosamente"}