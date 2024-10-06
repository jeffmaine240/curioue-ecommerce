from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'user_cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path(f'<int:product_id>/{_('add')}', views.add_product_to_cart, name='cart_add'),
    path(f'<int:product_id>/{_('remove')}', views.remove_all_product_item_from_cart, name='cart_remove'),
]