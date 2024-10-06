from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from coupon.models import Coupon
from shop.models import Product

from decimal import Decimal

# Create your models here.
class Order(models.Model):
    coupon = models.ForeignKey(Coupon, verbose_name=_('coupon'), related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(_('discount'),default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    stripe_id = models.CharField(_('stripe id'), max_length=250, blank=True)
    first_name = models.CharField(_('first name'), max_length=250)
    last_name = models.CharField(_('last name'), max_length=250)
    email = models.EmailField(_('e-mail'), max_length=254)
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=250)
    city = models.CharField(_('city'),max_length=250)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    paid = models.BooleanField(_('paid'), default=False)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.address
    
    def get_stripe_url(self):
        if self.stripe_id:
            if '_test_' in settings.STRIPE_SECRET_KEY:
                path = '/test/'
            else:
                path = '/'
            return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
        else:
            return ''
    
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        if self.discount:
            total = self.get_total_cost_before_discount()
            discount_amount = total * (self.discount / Decimal(100))
            return discount_amount
        return Decimal(0)
    
    def get_total_cost(self):
        total = self.get_total_cost_before_discount()
        discount_amount = self.get_discount()
        return total - discount_amount



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('order'))
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE,  verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.product)

    def get_cost(self):
        return self.quantity * self.unit_price