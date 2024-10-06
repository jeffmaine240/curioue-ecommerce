from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'coupon'
urlpatterns = [
    path(_('apply/'), views.coupon_apply, name='coupon_apply'),
]
