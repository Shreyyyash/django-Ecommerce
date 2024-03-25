from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORY_CHOICES=(
    ('cricket','cricket'),
    ('football','football'),
    ('badminton','badminton'),
    ('tennis','tennis'),
)
BRAND_CHOICES=(
    ('nike','nike'),
    ('adidas','adidas'),
    ('puma','puma'),
    ('SG','SG'),
    ('MRF','MRF'),
    ('NB',"NB"),
    ('Nivia','Nivia'),
    ('Mystic','Mystic'),
    ('Thrax','Thrax'),
    ('Cosco','Cosco')
)
STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES,max_length=255)
    description = models.TextField(default=True,null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(choices=BRAND_CHOICES,max_length=255)
    description = models.TextField(default=True,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title=models.CharField(max_length=50)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='my_products')
    
    def __str__(self) -> str:
        return self.title

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField( max_length=50)
    landmark=models.CharField( max_length=50)
    city=models.CharField( max_length=50)
    state=models.CharField(max_length=50,choices=STATE_CHOICES)
    pin_code=models.IntegerField()
    mobile=models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=50,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=50,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=50,blank=True,null=True)
    paid=models.BooleanField(default=False)

STATUS_CHOICES={
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On way','On way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
}
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=40, choices= STATUS_CHOICES,default='Pending')
    payment=models.ForeignKey(Payment,on_delete= models.CASCADE,default='')

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)