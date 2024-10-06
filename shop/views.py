from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from user_cart.forms import ProductAddToCart

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(availability=True)
    categories = Category.objects.all()
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
            )
        print(category)
        products = Product.objects.filter(category=category)

    return render(request, "shop/product/list.html", {
        'products': products,
        'categories': categories,
        'category': category
    })
 
def product_detail(request, product_id, product_slug):
    '''To get product details by checking the database with the product_id, product_slug, and its availability'''
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        availability=True,
        id=product_id,
        translations__language_code=language,
        translations__slug=product_slug
        )
    form = ProductAddToCart()
    return render(request, "shop/product/detail.html", {'product':product, 'cart_product_form': form})
