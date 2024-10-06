from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views
from . import webhook

app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.process, name='process'),
    path(_('completed/'), views.completed, name='completed'),
    path(_('cancelled'), views.cancelled, name='cancelled'),
]
