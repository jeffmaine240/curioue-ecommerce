from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings


from .forms import CouponApplyForm
from .models import Coupon
# Create your views here.

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = get_object_or_404(
                Coupon,
                code=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True)
            request.session[settings.COUPON_ID] = coupon.id
        except Coupon.DoesNotExist:
            request.session[settings.COUPON_ID] = None
    return redirect('user_cart:cart_detail')