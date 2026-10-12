from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.serializers import python

from .models import Car, SellerProfile , CustomerReview, CarSale

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

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Review',
        }
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this seller...',
            }),
        }

class CarSaleForm(forms.ModelForm):
    class Meta:
        model = CarSale
        fields = ['agreed_price']
        labels = {
            'agreed_price': 'Proposed Purchase Price (KSh)',
        }
        widgets = {
            'agreed_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
            }),
        }