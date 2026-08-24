import requests
from django.conf import settings


def get_productos():
    try:
        response = requests.get(
            f"{settings.TECHGEAR_API_BASE_URL}/productos",
            timeout=settings.TECHGEAR_API_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []


def get_producto(producto_id):
    try:
        response = requests.get(
            f"{settings.TECHGEAR_API_BASE_URL}/productos/{producto_id}",
            timeout=settings.TECHGEAR_API_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_pedidos():
    try:
        response = requests.get(
            f"{settings.TECHGEAR_API_BASE_URL}/pedidos",
            timeout=settings.TECHGEAR_API_TIMEOUT,
        )
        response.raise_for_status()
        pedidos = response.json()
    except requests.RequestException:
        return []

    # Enriquecer cada detalle de pedido con el nombre del producto
    productos = get_productos()
    mapa = {p["id"]: p["nombre"] for p in productos}
    for pedido in pedidos:
        for item in pedido.get("productos", []):
            item["producto_nombre"] = mapa.get(item["producto_id"], item["producto_id"])
    return pedidos


def crear_pedido(cliente, items):
    detalle = []
    for item in items:
        producto = get_producto(item["producto_id"])
        if not producto:
            return {"ok": False, "detail": "Producto no encontrado"}
        detalle.append(
            {
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"],
                "precio_unitario": producto["precio"],
            }
        )
    total = round(sum(d["precio_unitario"] * d["cantidad"] for d in detalle), 2)
    payload = {"cliente": cliente, "productos": detalle, "total": total}
    try:
        response = requests.post(
            f"{settings.TECHGEAR_API_BASE_URL}/pedidos",
            json=payload,
            timeout=settings.TECHGEAR_API_TIMEOUT,
        )
        return {
            "ok": response.ok,
            "status": response.status_code,
            "detail": response.json().get("detail")
            if not response.ok and response.headers.get("content-type", "").startswith("application/json")
            else ("Pedido creado exitosamente" if response.ok else "Error al crear el pedido"),
            "data": response.json() if response.ok else None,
        }
    except requests.RequestException as exc:
        return {"ok": False, "detail": f"No se pudo conectar con la API: {exc}"}