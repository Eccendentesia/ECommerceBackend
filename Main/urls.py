from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views  import *

urlpatterns = [
   path('register/',UserRegister.as_view()),
   path('login/',UserLogin.as_view()),
   path('admin/category/' , AddCategory.as_view()),
   path('admin/product/', AddProduct.as_view()),
   path("p_random/" , Send_Random),
   path('cart/',Cart.as_view()),
   path('get_cart_item/<int:id>',get_cart_item),
   path('delete_cart_item/<int:id>',delete_cart_item),
   path('update_cart_quantity/',update_cart_quantity),
   path('payment_info/',set_payment_info),
   path('send_order/<int:id>',send_order),
   path('order_detail/<str:id>/',get_order_detail)
   
]