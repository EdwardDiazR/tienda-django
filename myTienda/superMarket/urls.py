from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index,name="home"),
    path('login',views.login,name='login'),
    path('logout',views.cerrarSesion,name='login'),
    path("anadirProductos",views.anadirProductos, name='anadirProductos'),
    path("producto/<str:slug>/<int:id>",views.detalleProducto,name='detalle'),
    path("resultado/",views.search, name="busqueda"),
    path("categorias/<str:slug>",views.categoria,name='categoria'),
    path("carrito",views.carrito,name="carrito"),
    path("addToCart/<int:id>",views.anadirAlCarrito),
    path("deleteFromCart/<int:id>",views.eliminarDelCarrito),
    path("addq/<int:id>",views.add_quantity),
    path("restq/<int:id>",views.rest_quantity)


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)