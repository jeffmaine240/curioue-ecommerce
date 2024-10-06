from .cart_config import UserCart

def cart(request):
    return {'cart': UserCart(request)}