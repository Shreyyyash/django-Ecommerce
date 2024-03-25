from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django import forms 
from .models import Customer,Review

class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(label='Username', min_length=5, max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))  
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 

class UserLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':"current-password",'strip':False}))

class UserPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class UserCustomerForm(forms.ModelForm):  
    class Meta:
        model = Customer
        fields = '__all__'
        exclude= ('user',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'landmark':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'pin_code':forms.NumberInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
        }
    
class UserPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':"form-control"}))

class UserPasswordResetConfirm(SetPasswordForm):
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets={
            'rating':forms.Select(attrs={'class':'form-control'}),
            'review':forms.TextInput(attrs={'class':'form-control'}),
        }