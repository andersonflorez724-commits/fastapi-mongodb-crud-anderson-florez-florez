from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("crear-pedido/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/", views.ver_pedidos, name="ver_pedidos"),
]