from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self , u_email , password =None , **extra_fields ):
        email = self.normalize_email(u_email)
        user = self.model(u_email=email , **extra_fields )
        user.set_password(password)
        user.save()
        return user 
    def create_superuser(self , u_email , password=None , **extra_fields):
        user = self.create_user(u_email ,password , **extra_fields)
        user.is_staff = True 
        user.is_superuser = True 
        user.save()
        return user

class UserModel(AbstractBaseUser , PermissionsMixin):
    u_name = models.CharField(max_length = 100 , default='user_none')
    u_email = models.EmailField( unique = True )
    u_number = models.IntegerField()
    is_active = models.BooleanField(default = True )
    is_staff = models.BooleanField(default = False )
    created_at = models.DateTimeField(auto_now_add = True )

    objects = UserManager()
    
    USERNAME_FIELD='u_email'
    REQUIRED_FIELDS= ['u_name','u_number']

class Category(models.Model):
    c_name = models.CharField(max_length = 150)
    c_created = models.DateTimeField(auto_now_add = True , blank = True , null = True )
    c_updated = models.DateTimeField(auto_now = True , blank = True  , null = True  )

    def __str__(self ):
       return self.c_name
     
class Product(models.Model):
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    p_name = models.CharField(max_length = 150 )
    p_price = models.DecimalField(max_digits = 10 , decimal_places = 2 )
    p_description = models.TextField()
    p_image = models.ImageField(upload_to = "Products" , blank= True , null = True )
    p_stock = models.IntegerField( default=0)
    p_avail = models.BooleanField(default = False )
    p_created = models.DateTimeField(auto_now_add = True  )
    p_updated = models.DateTimeField(auto_now = True )
    
    def __str__(self):
        return f'{self.p_name},{self.p_price}'
  
class CartModel(models.Model):
    cart_user = models.ForeignKey(UserModel , on_delete = models.CASCADE)
    cart_product = models.ForeignKey(Product , on_delete = models.CASCADE)
    cart_quantity = models.PositiveIntegerField()
    cart_placed = models.BooleanField(default=  False)
    cart_created = models.DateTimeField(auto_now_add = True  )
    cart_updated = models.DateTimeField(auto_now = True )   
    order_number = models.CharField(max_length = 200 , default="999999999")
   

class OrderModel(models.Model):
    user = models.ForeignKey(UserModel , on_delete = models.CASCADE)
    address = models.TextField()
    number = models.CharField(max_length=200,null=True)
    order_time = models.DateTimeField(auto_now_add=True )
    final_status = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.user},{self.address},{self.number},{self.order_time}"
    
class FoodTrackingModel(models.Model):
    order = models.ForeignKey(OrderModel , on_delete = models.CASCADE)
    remark = models.CharField(max_length = 100 , null = True )
    status = models.CharField(max_length = 100 , null = True)
    status_date = models.DateTimeField(auto_now_add = True )
    order_cancelled = models.BooleanField(null = True , default = False)

    def __str__(self):
        return f"{self.order},{self.status}"
    
class PaymentModel(models.Model):
    payment_choices = [('cod',"Cash on delivery "),('online',"online payment")]

    user = models.ForeignKey(UserModel , on_delete = models.CASCADE)
    order_number = models.CharField(max_length = 100 )
    payment_mode = models.CharField(max_length = 20 ,choices = payment_choices )
    card_number = models.CharField(max_length = 20 , null = True ,blank = True  )
    card_expiry = models.CharField(max_length =20 , null = True , blank = True )
    cvv  = models.CharField(max_length = 3 , null = True , blank  = True )
    payment_date = models.DateTimeField(auto_now_add = True )

class ReviewModel(models.Model):
    user = models.ForeignKey(UserModel , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at  = models.DateTimeField(auto_now_add = True )

    def __str__(self):
        return f"{self.user},{self.comment},{self.careted_at}"

class WishListModel(models.Model):
    user = models.ForeignKey(UserModel , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    class Meta:
        unique_together = ("user",'product')
