from django.forms import forms,ModelForm
from .models import Product
from django import forms

class ProductoForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','product_price','product_category','product_brand','product_size','product_supplier','product_image','is_inOffer']
        
class LoginForm(forms.Form):
    
    username= forms.CharField(max_length=100,label="Usuario",required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña",required=True)