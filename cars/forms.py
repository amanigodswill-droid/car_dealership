from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Car, SellerProfile 

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price', 'description', 'image']
        labels = {'image': 'Image',}

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'id': 'id_password1',
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'id': 'id_password2',
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['phone', 'location']
        labels = {
            'phone': 'Phone Number',
            'location': 'Your Location',
        }