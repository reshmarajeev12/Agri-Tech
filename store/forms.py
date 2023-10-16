from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from store.models import Product
from django.core.validators import RegexValidator



CHOICE = [('user', 'no'),('farmer','yes')]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message='Enter a valid 10-digit phone number.')])
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']
        
    
    
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'digital', 'feature','link',]