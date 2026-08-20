from django.shortcuts import render, redirect
from django.contrib import messages

from .services import get_productos, crear_pedido


def catalogo(request):
    productos = get_productos()
    return render(request, "catalogo/catalogo.html", {"productos": productos})


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

        resultado = crear_pedido(cliente, [{"producto_id": producto_id, "cantidad": cantidad}])

        if resultado["ok"]:
            messages.success(request, resultado["detail"])
            return redirect("catalogo")

        messages.error(request, resultado["detail"])
        return redirect("crear_pedido")

    productos = get_productos()
    return render(request, "catalogo/crear_pedido.html", {"productos": productos})