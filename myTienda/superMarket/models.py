from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import os
import decimal
from math import ceil,floor

# Create your models here.


class Usuario(models.Model):
    username=models.CharField(primary_key=True,verbose_name='username',max_length=100)
    user_name=models.CharField(max_length=100,null=True,blank=True)
    user_last= models.CharField(max_length=100,null=True,blank=True)
    user_dob= models.DateField(null=True,blank=True)
    user_email=models.EmailField(null=True,blank=True)
    user_password=models.CharField(max_length=100)

class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=True,null=True)
    slug=AutoSlugField(populate_from='category_name',default='')
    category_image=models.ImageField(upload_to='category/',null=True,blank=True) 

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural='Categoria'
class Product(models.Model):

    CURRENCY_CHOICES = [('DOP', 'RD$')]
    product_id=models.AutoField(auto_created = True,
                  primary_key = True,
                  serialize = False, 
                  verbose_name ='product_id',
                  unique=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=19,decimal_places=2)
    product_category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    product_brand=models.CharField(max_length=100) 
    product_size=models.CharField(max_length=100)
    product_supplier=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to='pics/',null=True,blank=True) 
    product_slug = AutoSlugField(populate_from='product_name',default='')
    is_inOffer=models.BooleanField(default=False,null=False)
    discount_percentage=models.DecimalField(max_digits=5,decimal_places=2,default=0,blank=True)
    offer_final_price=models.DecimalField(max_digits=10,decimal_places=2,max_length=5)
    
    def offer_final_price(self):
        if self.is_inOffer == True:
            discount = round((self.product_price - (self.product_price * decimal.Decimal(self.discount_percentage / 100))))
            final = decimal.Decimal("{:.2f}".format(discount))
            self.product_price=final
            return final
        elif self.is_inOffer == True and self.discount_percentage == 0:
            self.is_inOffer == False
    def __int__(self):
         return self.product_id

class Cart(models.Model):
    cart_id=models.AutoField(auto_created = True,
                  primary_key = True,
                  serialize = False, 
                  verbose_name ='cart_id',
                  )
    cart_owner=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True,blank=True)
    isPaid = models.BooleanField(default=False)

    #Model Functions
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for c in cart_items:
            price.append(decimal.Decimal(c.get_item_price()) * decimal.Decimal(c.get_item_quantity()))

        return sum(price)
    def get_cart_count(self):
        cart_items = self.cart_items.all()
        return cart_items.count()
            
        
class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    item_name = models.CharField(max_length=100,null=True,blank=True)
    item_image=models.ImageField(null=True,blank=True)
    item_quantity = models.IntegerField(null=True,blank=True,default=1)

    #Model functions
    def item_name(self):
         return self.product.product_name
    def item_image(self):
        return self.product.product_image
    def get_item_price(self):
        self.item_price = self.product.product_price
        return self.item_price
    def get_item_category(self):
        return self.product.product_category
    def get_item_quantity(self):
        return self.item_quantity
    def item_slug(self):
        return self.product.product_slug
 