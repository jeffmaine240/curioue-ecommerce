from django.conf import settings

from decimal import Decimal
from shop.models import Product
from coupon.models import Coupon

class UserCart:
    '''Always refer back to the cart created in session'''
    def __init__(self, request):
        self.session = request.session
        # print(self.session)
        user_cart = self.session.get(settings.CART_NAME)
        if not user_cart:
            self.session[settings.CART_NAME] = {}
            user_cart =  self.session.get(settings.CART_NAME)
        self.cart = user_cart
        self.coupon_id = self.session.get('coupon_id')

        
    def __iter__(self):
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['product'].price)
            item['total_price'] = (Decimal(item['price']) * item['quantity'])
            yield item

    def save(self):
        self.session.modified = True


    def add(self, product, quantity, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def remove_one(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 0:
            self.cart[product_id]['quantity'] -= 1
        self.save()


    def remove_all(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def clear_cart(self):
        del self.session[settings.CART_NAME]
        if self.coupon:
            del self.session[settings.COUPON_ID]
        self.save()

    def __len__(self):
        total_product = 0
        for product in self.cart.values():
            total_product += product['quantity']
        return total_product

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None
    
    def get_discount(self):
        if self.coupon:
            total = self.get_total_price()
            discount_amount = total * (self.coupon.discount / Decimal(100))
            return discount_amount
        return Decimal(0)
    
    def get_price_after_discount(self):
        total = self.get_total_price()
        discount_amount = self.get_discount()
        return total - discount_amount


    

            





