from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review
)


def home(request):
    products = Product.objects.all().annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews")
    ).order_by("-id")

    return render(request, "index.html", {"products": products})


def account(request):
    return render(request, 'account.html') 


def product_details(request, id):
    product = get_object_or_404(
        Product.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        ),
        id=id
    )

    return render(request, "product-details.html", {"product": product})



@login_required(login_url='login')  # redirect to login if not logged in
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # Increment quantity if already in cart
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.title} added to cart!")
    return redirect(request.META.get('HTTP_REFERER', ''))


@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Calculate total amount
    total = sum([item.get_total() for item in cart.items.all()])
    
    return render(request, 'cart_detail.html', {'cart': cart, 'total': total})


@login_required(login_url='login')
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


# Custom decorator for showing message before redirect
def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in first!")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper