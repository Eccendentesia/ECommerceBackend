from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens  import RefreshToken
from rest_framework.parsers  import MultiPartParser , FormParser
from rest_framework.permissions import IsAuthenticated , AllowAny 
from .models import *
from .serialize import * 
import random 
# Create your views here.

class UserRegister(APIView):
    def post(self , request):
        try:
             serialize = UserSerializer(data = request.data)
             if serialize.is_valid() :
                 serialize.save()
                 return Response({
                     'message':"User Registered Successfully",
                     "status":200,
                     "data":serialize.data
                 } )
             return Response({
                 "message":"Failed while registering user ",
                 "status":400
             })
        except Exception as err :
            print(err)
    
class UserLogin(APIView):
    def post(self , request):
        email = request.data.get('u_email')
        password = request.data.get("password")
        user = UserModel.objects.filter(u_email=email ).first()
        print(user.id)
        if not user:
            return Response({
                'message':"User is not registered , register first",
                'status':400
            },status =400)
        if not user.check_password(password):
             return Response({
                'message':"Password is incorrect",
                'status':400
            },status =400)
        refresh = RefreshToken.for_user(user)
        return Response({
                'message':'User Logged in successfully',
                'status':200 ,
                'access':str(refresh.access_token),
                'refresh':str(refresh),
                'userId':user.id
            } ,status = 200)
    

class AddCategory(APIView):
    parser_classes =(MultiPartParser , FormParser)
    def post(self , request):
        print(request.data)
        serialize = CategorySerializer(data = request.data)
        if serialize.is_valid():
            serialize.save()
            print(serialize.data)
            return Response({
             "message":"Category Added successfully ",
             "status":200

            })
        
        return  Response({
             "message":"Some error occurred  ",
             "status":400

            })
    def get(self , request):
        data = Category.objects.all()
        serialize = CategorySerializer(data , many = True )
        return Response({
            "message":"data from category",
            "data":serialize.data 
        })
class AddProduct(APIView):
    parser_classes =(MultiPartParser , FormParser)
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self , request):
      try:
        serialize = ProductSerializer(data = request.data )
        print(request.data)
        if serialize.is_valid():
            serialize.save()
            return Response({
                "message":"Product Added Successfully"
            } , status = 200)
      except Exception as e : 
        print(e)
        return Response({
                "message":"Some error in Serializer"
            } , status = 400)
    
    def get(self , request ):
      try:
        data = Product.objects.all()
        serialize = ProductSerializer(data , many = True  , context ={"request" : request})
        return Response({
            "message":"Product Sent Successfully",
            "data":serialize.data 
        })
      except Exception as e:
          print(e)

@api_view(['GET'])
def Send_Random(request):
    data = list(Product.objects.all())
    random.shuffle(data)
    _data = data[:3]
    serialize = ProductSerializer(_data , many= True , context={'request':request})
    return Response({
        "message":"Send the data ",
        "data":serialize.data
    })

class Cart(APIView):
    def post(self , request):
        try:
           product = Product.objects.get(id = request.data.get('cart_product'))
           user = UserModel.objects.get(id = request.data.get('cart_user'))
          
           order , created = CartModel.objects.get_or_create(
               cart_user = user ,
               cart_placed = False , 
               cart_product = product ,
               defaults ={"cart_quantity":1}
           )
           if not created :
               order.cart_quantity += 1 
               order.save()
               return Response({
                "message":"updated existing product to cart "
              })
           return Response({
               "message":"Product added to cart "
           })
        except Exception as e :
            print(e)
            return Response(
                {
                    "error": "Failed to add product to cart",
                    "details": str(e)
                },
            )
    
@api_view(["GET"])
def get_cart_item(request , id ):
        user = UserModel.objects.get(id = id)
        data = CartModel.objects.filter(cart_user =user , cart_placed = False ).select_related('cart_product')
        serialize = CartSerializer(data , many = True , context ={'request':request})
        return Response({
            "message":"Data send to frontend",
            'data':serialize.data 
        })

@api_view(['delete'])
def delete_cart_item(request , id):
    data = CartModel.objects.get(id = id)
    data.delete()
    return Response({
        'message':"Cart Item deleted Successfully"
    } , status = 200)

@api_view(['PUT'])
def  update_cart_quantity(request):
    cartId  = request.data.get('cart_id')
    cartNewQuantity = request.data.get('cart_quantity')
    try:
       cart = CartModel.objects.get(id = cartId, cart_placed = False)
       cart.cart_quantity = cartNewQuantity
       cart.save()
       print('cart updated' , cart.cart_product , cart.cart_quantity)
       return Response({
           'message':"Cart Updated "
   
       })
    except Exception as e :
         return Response({
           'message':"Cart Update have  issue  "
   
       })
    
#payment api 
def get_order_num():
    while True :
        num = str(random.randint(1000000000,9999999999))
        if not OrderModel.objects.filter(number = num).exists():
            return num 

@api_view(['POST'])
def set_payment_info(request):
        id = request.data.get('user_id')
        addr = request.data.get('addr')
        mode = request.data.get('mode')
        cnum = request.data.get('card_number')
        cexpiry = request.data.get('card_expiry')
        ccvv = request.data.get('card_cvv')
        try:
              user = UserModel.objects.get(id = id )            
              order = CartModel.objects.filter(cart_user = user, cart_placed = False)
              order_num = get_order_num()
              order.update( order_number = order_num , cart_placed =True )
              
              OrderModel.objects.create(
                  user = user, address  = addr , number = order_num  
              )
              PaymentModel.objects.create(user = user , order_number = order_num , 
                    payment_mode = mode ,
                    card_number = cnum if mode == "online" else None ,
                    card_expiry= cexpiry if mode == "online" else None ,
                    cvv  = ccvv if mode == "online" else None )
              return Response({
                  'message':"Order placed Successfully",
                  "status":200
              })
              
        except Exception as e:
            return Response({
                "message":str(e)
            })
        
#sending order data to frontend 
@api_view(['GET'])
def send_order(request , id):
    data = OrderModel.objects.filter(user = id)
    serialize = OrderSerializer(data , many = True  )   
    return Response({
            'message':"Sent order data to frontend",
            'data':serialize.data
        })


#getting order detail after displaying on order section
@api_view(['GET'])
def get_order_detail(request , id ):
    data = CartModel.objects.filter(order_number = id , cart_placed = True ).select_related('cart_product')
    serialize = CartSerializer(data , many=True , context={'request':request} )
    print(serialize.data)
    return Response({
        'message':"detail sent",
        'data':serialize.data
    })
