from django.contrib import admin
from .models import Category,Brand,Product,Customer,Cart,Order,Payment,Wishlist,Review
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discount_price','description','category','brand','product_image']
    search_fields=['title','category__name','brand__name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=['id','name','description']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','landmark','city','state','pin_code','mobile']  

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','products','quantity','total_cost']
    
    def products(self, obj):
        link = reverse("admin:myapp_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">Edit {}</a>', link, obj.product.title)

@admin.register(Wishlist)
class Admin(admin.ModelAdmin):
    list_display=['id','user','product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','products','quantity','ordered_date','status','payments']
    def products(self, obj):
        link = reverse("admin:myapp_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">Edit {}</a>', link, obj.product.title)
    
    def payments(self,obj):
        link = reverse('admin:myapp_payment_change',args=[obj.payment.pk])
        return format_html('<a href="{}">Edit {}</a>',link,obj.payment.razorpay_payment_id)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['id','user','product','rating','review','created_at']


