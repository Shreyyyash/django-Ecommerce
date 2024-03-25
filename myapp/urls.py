
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from .forms import UserPasswordChangeForm,UserPasswordResetForm,UserPasswordResetConfirm
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.home,name='home'),
    path('category/<slug:value>/',views.ProductView.as_view(),name='category'),
    path('category/products/<int:id>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('userregistration/',views.UserRegistration.as_view(),name="user-registration"),

    # login-logout
    path('loginuser/',views.UserLogin.as_view(),name='login-user'),
    path('logoutuser/', auth_view.LogoutView.as_view(next_page='login-user'),name='logout-user'),

    # address-profile
    path('customer-profile/',views.CustomerProfileView.as_view(),name='customer-profile'),
    path('customer-address/',views.CustomerAddressView.as_view(),name='customer-address'),
    path('update-address/<slug:pk>/',views.CustomerAddressUpdateView.as_view(),name='update-address'),
    path('delete-address/<slug:pk>/',views.CustomerAddressDeleteView.as_view(),name='delete-address'),

    #password
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name='myapp/password_change.html',success_url='/password-change-done/',form_class=UserPasswordChangeForm),name='password-change'),
    path('password-change-done/',auth_view.PasswordChangeDoneView.as_view(template_name='myapp/password_change_done.html'),name='password-change-done'),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='myapp/password_reset.html',form_class=UserPasswordResetForm),name='password-reset'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html',form_class=UserPasswordResetConfirm ,success_url=reverse_lazy('password_reset_complete')), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name ='password_reset_complete'),
    
    # cart
    path('add-to-cart/',views.AddToCart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('delete-cart-item/<int:id>/',views.removeFromCart,name='delete-cart-item'),
    path('plus_cart/',views.PlusCart,name='plus-cart'),
    path('minus_cart/',views.MinusCart),

    #wishlist
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    path('wishlist/',views.ShowWishlist,name='wishlist'),

    # checkout
    path('checkout/',views.CheckOut.as_view(),name='checkout'),

    # paymentdone
    path('paymentdone/',views.PaymentDone,name='paymentdone'),
    path('orders/',views.Orders,name='orders'),

    #search
    path('search/',views.SearchProduct,name='search'),

    #review
   path('review/delete/<int:id>/',views.DeleteReview,name="delete-review"),
   path('review/edit/<int:id>/',views.EditReview,name='edit-review'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

