from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views import View
from .models import Product,Category,Customer,Cart,Payment,Order,Wishlist,Review
from django.core.paginator import Paginator
from django.core.cache import cache
import random
from .forms import UserRegistrationForm,UserLoginForm,UserCustomerForm,ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic.edit import FormView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.db.models import Q
import razorpay
from ecommerce_site import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import os
from dotenv import load_dotenv

# Create your views here.
def home(request):
    prod=list(Product.objects.all())
    random_products = random.sample(prod, 6)
    cache_product=cache.get_or_set('random_products', random_products, 300) 
    context = {'random_products': cache_product}
    return render(request, 'myapp/home.html', context)

def contact(request):
    return render(request,'myapp/contact.html')
    
def about(request):
    return render(request,'myapp/about.html')

class ProductView(View):
    
    def get(self,request,value):
        # category=Category.objects.get(name=value)
        category = get_object_or_404(Category, name=value)
        products=Product.objects.filter(category=category)

        # Paginate the Products
        paginator=Paginator(products,8)
        page = request.GET.get('page', 1)
        items = paginator.page(page)
        
        context = {
        "products": items,
        }
        return render(request,'myapp/product.html',context)
    
class ProductDetailView(View):
    def get(self, request, id):       
        product =Product.objects.select_related('brand').get(pk=id)
        
        # To show if there are products in wishlist else not        
        wishlist=Wishlist.objects.filter(product=product)
        
        # review form
        revform=ReviewForm()
        order=Order.objects.filter(product=product,status="Delivered")
        # review=Review.objects.filter(product=product).order_by('-created_at')
        if request.user.is_authenticated:
            current_user_review=Review.objects.filter(product=product,user=request.user).order_by('-created_at')
            other_user_review=Review.objects.exclude(user=request.user).filter(product=product).order_by('-created_at')
            review = list(current_user_review) + list(other_user_review)
        review=Review.objects.filter(product=product)
        context = {
            "product_detail": product,
            "wishlist":wishlist,
            'revform':revform,
            'order':order,
            'review':review,
        }
        return render(request, 'myapp/product_detail.html', context)
    
    def post(self,request,id):
        product =Product.objects.select_related('brand').get(pk=id)
        revform=ReviewForm()
        revform=ReviewForm(request.POST)
        
        if revform.is_valid():
            rating=revform.cleaned_data['rating']
            review=revform.cleaned_data['review']
            rev=Review(product=product,user=request.user,rating=rating,review=review).save()
        revform=ReviewForm()
        return redirect('product_detail', id=product.id)
        

class UserRegistration(View):
    def get(self,request):
        form=UserRegistrationForm()
        return render(request,'myapp/user_registration.html',{'form':form})

    def post(self,request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created Successfully!')
        return render(request,'myapp/user_registration.html',{'form':form})

class UserLogin(View):
    def get(self,request):
        form=UserLoginForm()
        return render(request,'myapp/user_login.html',{'form':form})
    
    def post(self,request):
        # use this parameters in obj-class or wont get login
        form=UserLoginForm(request=request,data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
        messages.success(request,'Login Failed')
        return render(request,'myapp/user_login.html',{'form':form})

  
class CustomerAddressView(FormView):
    form_class=UserCustomerForm
    template_name='myapp/customer_address.html'
    success_url='/customer-address/'

    def form_valid(self, form):
        detail = form.save(commit=False)
        detail.user = self.request.user
        detail.save()
        return super().form_valid(form)

 
class CustomerProfileView(View):
    def get(self,request):
        customer=Customer.objects.filter(user=self.request.user)
        return render(request,"myapp/user_profile.html",{'customer':customer})

  
class CustomerAddressUpdateView(UpdateView):
    form_class=UserCustomerForm
    template_name='myapp/address_update.html'
    success_url='/customer-profile/'
    model=Customer
    # fields=['name','landmark','city','state','pin_code','mobile']

 
class CustomerAddressDeleteView(DeleteView):
    model=Customer
    success_url='/customer-profile/'

@login_required   
def AddToCart(request):
    user=request.user
    prod_id=request.GET.get('prod_id')
    product=Product.objects.get(id=prod_id)
    
    # save to cart model
    cart=Cart(user=user,product=product)
    cart.save()   
    return redirect('cart')

@login_required 
def cart(request):
    user=request.user
    cart_item= Cart.objects.filter(user=user)

    amount=0
    shipping_charge=50
    for item in cart_item:
        value=item.product.discount_price * item.quantity
        amount=amount+value
    total_amount=amount+shipping_charge

    context={'cart_item':cart_item ,'amount':amount,'totalamount':total_amount}
    return render(request,'myapp/cart.html',context)


def removeFromCart(request,id):
    user=request.user
    cart=Cart.objects.get(user=user,pk=id)
    cart.delete()
    return redirect('cart')

def PlusCart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart_item=Cart.objects.filter(user=user)
        amount=0
        shipping_charge=50
        for item in cart_item:
            value=item.product.discount_price* item.quantity
            amount=amount+value
        total_amount=amount+shipping_charge

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount,
        }
        return JsonResponse(data)

def MinusCart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity>1:
            c.quantity-=1
            c.save()
        user=request.user
        cart_item=Cart.objects.filter(user=user)
        amount=0
        shipping_charge=50
        for item in cart_item:
            value=item.product.discount_price* item.quantity
            amount=amount+value
        total_amount=amount+shipping_charge

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount,
        }
        return JsonResponse(data)
    
@login_required
def plus_wishlist(request):
    ruser = get_object_or_404(User,id=request.user.id)
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        wishlist = Wishlist.objects.create(user=ruser, product=product)
        wishlist.save()
        return JsonResponse({'message': 'Added to Wishlist.'})
    
@login_required
def minus_wishlist(request):
    ruser = get_object_or_404(User,id=request.user.id)
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        wishlist = Wishlist.objects.get(user=ruser, product=product)
        wishlist.delete()
        return JsonResponse({'message': 'Removed from Wishlist.'})

@login_required 
def ShowWishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request,'myapp/wishlist.html',{'wishlist':wishlist})


class CheckOut(View):
    def get(self,request):
        user=request.user
        cart_item=Cart.objects.filter(user=user)
        add=Customer.objects.filter(user=user)
        amount=0
        shipping_charge=50
        for item in cart_item:
            value=item.product.discount_price* item.quantity
            amount=amount+value
        totalamount=amount+shipping_charge
        
        razoramount=int(totalamount*100)
        load_dotenv()
        RAZORPAY_API_KEY = os.getenv("RAZOR_KEY_ID")
        RAZORPAY_API_SECRET = os.getenv("RAZOR_KEY_SECRET")
        razor_key = RAZORPAY_API_KEY
        print(razor_key,RAZORPAY_API_KEY,RAZORPAY_API_SECRET)
        client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET))
        
        # client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={"amount":razoramount,"currency":"INR","receipt":"order_rcptid_11"}
        payment_response=client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        
        if order_status=='created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()
        
        return render(request,'myapp/checkout.html',locals())

@login_required 
def PaymentDone(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    print(cust_id)
    ruser=request.user.id
    user=request.user
    print(ruser,user)
    customer = get_object_or_404(Customer, id=cust_id)
    # customer=Customer.objects.get(id=cust_id)
    print(customer)
    # update payment satus
    
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()

    # save order details
    cart=Cart.objects.filter(user=ruser)
    for c in cart:
        Order.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                payment=payment
            )
        c.delete()
    return redirect('/orders/')

@login_required 
def Orders(request):
    order_placed=Order.objects.filter(user=request.user).select_related("payment",'product')
    return render(request,'myapp/orders.html',locals())

def SearchProduct(request):
    if request.method=="GET":
        name=request.GET.get("search")
        if name != "":
            product=Product.objects.select_related('category', 'brand').filter(Q(title__icontains=name) | Q(category__name__icontains=name) | Q(brand__name__icontains=name))
            results=product.count()
            # print(product)
            return render(request,'myapp/search.html',{'products':product,'results':results})
        else:
            return redirect('home')


def DeleteReview(request,id):
    rev=Review.objects.select_related('product').get(id=id)
    prod_id= rev.product.id
    
    if request.user == rev.user:  
        rev.delete()
        return redirect("product_detail",prod_id)
    else:
        return redirect("product_detail",prod_id)

def EditReview(request, id):
    rev = get_object_or_404(Review, id=id)
    prod_id=rev.product.id
    if request.method=="POST":
        revform=ReviewForm(request.POST,instance=rev)
        if revform.is_valid():
            revform.save()
            return redirect('product_detail',prod_id)
    else:
        revform=ReviewForm(instance=rev)
    return render(request,'myapp/edit_review.html',{'revform':revform})

