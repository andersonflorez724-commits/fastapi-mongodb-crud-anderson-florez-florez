from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    # CRUD Productos
    path("productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/<str:producto_id>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<str:producto_id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    # Pedidos
    path("crear-pedido/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/", views.ver_pedidos, name="ver_pedidos"),
    path("pedidos/<str:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
]