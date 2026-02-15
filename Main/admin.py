from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=("u_name","u_email","password","u_number")

class CategoryAdmin(admin.ModelAdmin):
    list_display =['c_name']

class ProductAdmin(admin.ModelAdmin):
    list_display =['category','p_name','p_price' ,'p_description','p_stock','p_avail','p_image']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','cart_user','cart_product','cart_quantity','order_number']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['address','number','order_time']
    
admin.site.register(UserModel ,UserAdmin)
admin.site.register(Category ,CategoryAdmin)
admin.site.register(Product , ProductAdmin)
admin.site.register(CartModel , CartAdmin)
admin.site.register(OrderModel , OrderAdmin)