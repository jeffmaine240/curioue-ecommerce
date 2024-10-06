from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from payment import webhook

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('cart/'), include('user_cart.urls', namespace='user_cart')),
    path(_('order/'), include('order.urls', namespace='order')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupon/'), include('coupon.urls', namespace='coupon')),
    path('rosetta/', include('rosetta.urls')),
    path('', include('shop.urls', namespace='shop')),
)

urlpatterns += [path('payment/webhook/', webhook.stripe_webhook, name='webhook')]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)