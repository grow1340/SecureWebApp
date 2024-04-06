"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Cart
from .forms import ItemForm, ContactForm
from .forms import RegistrationForm
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages





def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    item_list = Item.objects.all()

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'item_list' : item_list,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form, 'title':'Contact',
            'message':'Please Fill out the form and we will get back to you soon.',})



def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistrationForm()

    return render(request, 'app/register.html', {'form': form, 'title' : 'Create an Account'})

@login_required
def create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)  # Don't save to database yet
            item.user_id = request.user.id
            form.save()
            messages.success(request, 'Your item has been added!')
            return redirect('home') 
    else:
        form = ItemForm()
    return render(request, 'app/create.html', {'form': form, 'title' : 'Create a New Listing', 'message':'Please fill out the required fields.'})

@login_required
def cart(request):
    """View the user's cart."""
    assert isinstance(request, HttpRequest)

    total = 0.0

    try:
        # Retrieve the cart entry for the current user
        cart = Cart.objects.get(user_id=request.user.id)
       
        # Retrieve items from the items field of the Cart model
        items_in_cart_ids = cart.get_items()

        item_list = Item.objects.filter(id__in=items_in_cart_ids)

        for item in item_list:
            total += float(item.price)

    except Cart.DoesNotExist:
        # If the cart entry does not exist for the current user, set items_in_cart to an empty list
        item_list = []
       
       
    
    return render(
        request,
        'app/cart.html',
        {
            'title': 'Your Cart',
  
            'item_list' : item_list,

            'total': total,
        }
    )

@login_required
def add_to_cart(request, item_id):
    """Adds an item to the cart."""
    assert isinstance(request, HttpRequest)
    
    item = Item.objects.get(pk=item_id)
    
    try:
        cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        # Create a new cart entry for the user if it doesn't exist
        cart = Cart.objects.create(user_id=request.user.id, items=[])
    
    # Check if the item is already in the cart
    if cart and str(item.id) not in cart.items:
        # Add the item to the cart
        cart.add_item(item.id)
        cart.save()
    
    return redirect('cart')

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Check if the logged-in user is the owner of the item
    if request.user == item.user:
        item.delete()
        return redirect('home')
    else:
        return redirect('home')



 
@login_required   
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.INFO, "Hello world.")
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/account.html', {
        'form': form, 'title' : 'Account Management', 'message' : 'Fill in the following fields to change your password.'
    })