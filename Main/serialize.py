from rest_framework import serializers 
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','u_name','u_email','u_number','password']
        extra_fields={
            "password":{"write_only":True }
        }
        
    def create(self , validated_data):
       password = validated_data.pop('password', None)
       user = UserModel.objects.create_user( u_email=validated_data['u_email'],
         password=password, u_name=validated_data.get('u_name'),
           u_number=validated_data.get('u_number') )
       return user 
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category 
        fields ="__all__"

class ProductSerializer(serializers.ModelSerializer):
    p_image = serializers.ImageField(use_url = True, required = False  )
    category = serializers.StringRelatedField()
    class Meta :
        model = Product
        fields = ['id','category','p_name','p_price','p_description','p_image','p_stock','p_avail']

class CartSerializer(serializers.ModelSerializer):
    cart_product = ProductSerializer()
    class Meta:
        model = CartModel
        fields = ['id','cart_user','cart_product','cart_quantity' , 'cart_placed','order_number']

class OrderSerializer(serializers.ModelSerializer):
    final_status = serializers.SerializerMethodField()
    class Meta :
        model = OrderModel
        fields = ['id','address','number',"order_time",'final_status']
    
    def get_final_status(self , obj):
        return obj.final_status or "waiting for restuarent confirmation"