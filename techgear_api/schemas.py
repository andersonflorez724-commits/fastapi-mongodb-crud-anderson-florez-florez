from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Esquema para Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, description="El stock no puede ser negativo")

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: str

# Esquema para Pedido
class DetallePedido(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)
    precio_unitario: float

class PedidoBase(BaseModel):
    cliente: str
    productos: List[DetallePedido]
    total: float

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: str
    fecha: datetime = Field(default_factory=datetime.utcnow)