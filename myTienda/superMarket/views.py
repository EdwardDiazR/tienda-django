from django.shortcuts import render,redirect
from django.http import request,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Product,Category,Cart,CartItem,Usuario
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.shortcuts import  get_object_or_404
import requests
from django.db.models import F 
from django.db import connection
from django.contrib.auth.models import User



from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.

def index(request):
    if request.method == 'GET':
        ofertas = Product.objects.filter(is_inOffer = True)
        
        categorias = Category.objects.all()
        producto = Product.objects.raw('SELECT * FROM supertienda.supermarket_product;')
        
      
        print(request.user.is_authenticated)
        return render(request,'home/home.html',{
            "addProduct": ProductoForm,
            "ofertas": ofertas,
            "producto": producto,
            "categorias":categorias.order_by('?'),
            'isA':request.user.is_authenticated
        })
    
def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            
            try:
                user = authenticate(username=form.cleaned_data["username"].lower(), password=form.cleaned_data["password"])
                if user is not None:
                   
                    auth_login(request, user)
                    isA = request.user.is_authenticated
                    print(isA)
              
            
                    return HttpResponseRedirect('/',{
                        user,
                        isA
                        
                    })
                else:
                    return HttpResponse('algo mal')
            except:
                
                return HttpResponse('POST')
        else:
            return HttpResponse('hay algo mal')
    else:
        return render(request,'login/login.html',{
            "error": "Usuario o contraseña incorrectos",
            "LoginForm": LoginForm
        })
   
@login_required
def cerrarSesion(request):
    logout(request)
    isA = False
    print(isA)
    return HttpResponseRedirect('/',{
        isA 
    })
def search(request):
    busqueda = (request.GET.get("buscarProducto").lower())
    busqueda_categoria = Category.objects.filter(slug__istartswith=busqueda)
    if len(busqueda) == 0:
        return HttpResponse('Ofertas')
    elif len(busqueda_categoria):
        busqueda_categoria = Category.objects.filter(slug__istartswith=busqueda).get().slug
        codigo_busqueda_categoria = Category.objects.get(slug=busqueda_categoria).pk
        resultado=Product.objects.filter(product_slug__icontains=busqueda) | Product.objects.filter(product_brand__icontains=busqueda) | Product.objects.filter(product_supplier__icontains = busqueda) | Product.objects.filter(product_category=codigo_busqueda_categoria ).only("product_image")
    else:
        
        resultado=Product.objects.filter(product_name__icontains=busqueda) | Product.objects.filter(product_brand__icontains=busqueda) | Product.objects.filter(product_supplier__icontains = busqueda)

        
    return render(request,"resultados/resultados.html",{
    'busqueda': busqueda,
    'producto':resultado.order_by('is_inOffer'),
    'cantidadResultados':resultado.count(),
    'sinResultado': busqueda   
})


def detalleProducto(request,slug,id):
    producto = Product.objects.filter(product_id=id).get()
    ofertas = Product.objects.filter(is_inOffer = True)
    return render(request,"detail/detail.html",{
        "producto": producto,
        "slug":slug,
        "ofertas": ofertas,
        
    })
    

def anadirProductos(request):
    producto = Product.objects.all()
    if request.method == 'POST':
        newProductForm = ProductoForm(request.POST,request.FILES)
        print(Product.objects.all())
        if newProductForm.is_valid():
            newProductForm.cleaned_data['product_name'].upper()
            newProductForm.save()
            
        return redirect("/",{
        "addProduct": ProductoForm,
        "producto": producto
    })

@login_required
def carrito(request):
    print(request.user)
    isA = request.user.is_authenticated
    if isA:
        user = request.user
        owner = Usuario.objects.get(username=user)
        cart,_=Cart.objects.get_or_create(cart_owner=owner,isPaid=False)

        cart_items = CartItem.objects.raw(f'select id from supertienda.supermarket_cartitem WHERE cart_id = {cart.cart_id}')

        context = {'cart':cart,
                    'items': cart_items,  
                    'isA':isA}
        return render(request,"carrito/carrito.html",
         context
    )
    else:
     
        return HttpResponse('no hay usuario')
    print(connection.queries)

   
@login_required   
def anadirAlCarrito(request,id):
    user=request.user
    cart_owner = Usuario.objects.get(username=user)
    product = Product.objects.get(product_id=id)
    cart,_ = Cart.objects.get_or_create(cart_owner=cart_owner,isPaid=False)
    isInCart = CartItem.objects.filter(product=product,cart=cart)

    if isInCart:
        cartItem= CartItem.objects.get(product=product,cart=cart)
        cartItem.item_quantity += 1
        cartItem.save()
    else:    
        add_cart_items = CartItem.objects.create(cart = cart, product=product)
        add_cart_items.save()

  
    
    return HttpResponseRedirect(reverse("carrito"))

def eliminarDelCarrito(request,id):
    cartItem= CartItem.objects.get(id=id)
    cartItem.delete()

    return HttpResponseRedirect(reverse('carrito'))


def add_quantity(request,id):
   
   cartItem= CartItem.objects.get(id=id)
   cartItem.item_quantity += 1
   cartItem.save()
   return HttpResponseRedirect(reverse('carrito'))
   
def rest_quantity(request,id):
   
   cartItem= CartItem.objects.get(id=id)
   print(cartItem)
   if cartItem.item_quantity > 1:
        cartItem.item_quantity -= 1
  
       
  
   cartItem.save()
   return HttpResponseRedirect(reverse('carrito'))
   

def categoria(request,slug):
    codigo_categoria= Category.objects.get(slug__icontains=slug).pk
    resultado=Product.objects.filter(product_category=codigo_categoria)
    print(slug, codigo_categoria,resultado)
    return render(request,"resultados/resultados.html",{
  
    'producto':resultado.order_by('is_inOffer'),
    'cantidadResultados':resultado.count(),
    'busqueda':slug
    })


    