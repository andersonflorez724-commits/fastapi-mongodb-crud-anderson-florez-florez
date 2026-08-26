from django.shortcuts import render, redirect
from django.contrib import messages

from .services import (
    get_productos, get_producto, get_pedidos, get_pedido,
    crear_pedido as crear_pedido_api,
    crear_producto as crear_producto_api,
    actualizar_producto as actualizar_producto_api,
    eliminar_producto as eliminar_producto_api,
)


def catalogo(request):
    productos = get_productos()
    return render(request, "catalogo/catalogo.html", {"productos": productos})


def ver_pedidos(request):
    pedidos = get_pedidos()
    return render(request, "catalogo/ver_pedidos.html", {"pedidos": pedidos})


def crear_pedido(request):
    if request.method == "POST":
        cliente = request.POST.get("cliente", "").strip()
        producto_id = request.POST.get("producto_id", "").strip()
        cantidad = request.POST.get("cantidad", "1")

        if not cliente or not producto_id:
            messages.error(request, "Debe indicar el cliente y seleccionar un producto.")
            return redirect("crear_pedido")

        try:
            cantidad = int(cantidad)
        except ValueError:
            messages.error(request, "La cantidad debe ser un número entero.")
            return redirect("crear_pedido")

        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect("crear_pedido")

        resultado = crear_pedido_api(cliente, [{"producto_id": producto_id, "cantidad": cantidad}])

        if resultado["ok"]:
            messages.success(request, resultado["detail"])
            return redirect("catalogo")

        messages.error(request, resultado["detail"])
        return redirect("crear_pedido")

    productos = get_productos()
    return render(request, "catalogo/crear_pedido.html", {"productos": productos})


# ==================== CRUD PRODUCTOS ====================

def crear_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        precio = request.POST.get("precio", "0")
        stock = request.POST.get("stock", "0")

        if not nombre:
            messages.error(request, "El nombre del producto es obligatorio.")
            return redirect("crear_producto")

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            messages.error(request, "Precio y stock deben ser números válidos.")
            return redirect("crear_producto")

        resultado = crear_producto_api(nombre, descripcion, precio, stock)
        if resultado["ok"]:
            messages.success(request, resultado["detail"])
            return redirect("catalogo")

        messages.error(request, resultado["detail"])
        return redirect("crear_producto")

    return render(request, "catalogo/crear_producto.html")


def editar_producto(request, producto_id):
    producto = get_producto(producto_id)
    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect("catalogo")

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        precio = request.POST.get("precio", "0")
        stock = request.POST.get("stock", "0")

        if not nombre:
            messages.error(request, "El nombre del producto es obligatorio.")
            return redirect("editar_producto", producto_id=producto_id)

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            messages.error(request, "Precio y stock deben ser números válidos.")
            return redirect("editar_producto", producto_id=producto_id)

        resultado = actualizar_producto_api(producto_id, nombre, descripcion, precio, stock)
        if resultado["ok"]:
            messages.success(request, resultado["detail"])
            return redirect("catalogo")

        messages.error(request, resultado["detail"])
        return redirect("editar_producto", producto_id=producto_id)

    return render(request, "catalogo/editar_producto.html", {"producto": producto})


def eliminar_producto(request, producto_id):
    if request.method == "POST":
        resultado = eliminar_producto_api(producto_id)
        if resultado["ok"]:
            messages.success(request, resultado["detail"])
        else:
            messages.error(request, resultado["detail"])
    return redirect("catalogo")


def detalle_pedido(request, pedido_id):
    pedido = get_pedido(pedido_id)
    if not pedido:
        messages.error(request, "Pedido no encontrado.")
        return redirect("ver_pedidos")
    return render(request, "catalogo/detalle_pedido.html", {"pedido": pedido})