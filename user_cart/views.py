from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse

from shop.models import Product
from .cart_config import UserCart
from .forms import ProductAddToCart
from coupon.forms import CouponApplyForm


# Create your views here.

@require_POST
def add_product_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductAddToCart(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart = UserCart(request)
    cart.add(product, cd['quantity'], cd['override'])
    return redirect(reverse('user_cart:cart_detail'))

@require_POST
def remove_one_product_item_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = UserCart(request)
    cart.remove_one(product)
    return redirect(reverse('user_cart:cart_detail'))

@require_POST
def remove_all_product_item_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = UserCart(request)
    cart.remove_all(product)
    return redirect(reverse('user_cart:cart_detail'))

def clear_cart(request):
    cart = UserCart(request)
    cart.clear_cart()
    return redirect(reverse('user_cart:cart_detail'))

def cart_detail(request):
    form = CouponApplyForm()
    cart = UserCart(request)
    for item in cart:
        item['update_item_quantity_form'] = ProductAddToCart(initial={'quantity': item['quantity'], 'override': True})
        print('item_price:', item['price'])
        print('item_total_price:', item['total_price'])
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': form})

    

    


