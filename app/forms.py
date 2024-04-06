"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Item, ContactMessage



class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Email'
                             }))
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'User name'
                               }))
    password1 = forms.CharField(label=_("Password1"),
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Password'
                                }))
    password2 = forms.CharField(label=_("Password2"),
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Confirm Password'
                                }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
 


class ItemForm(forms.ModelForm):

    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    description = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    price = forms.DecimalField(min_value=1.00, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}))
    #image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Item
        fields = ['title', 'description', 'price']
        #fields = ['title', 'description', 'price', 'image']

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}))

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']