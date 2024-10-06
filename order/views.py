from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.template.loader import get_template

from io import BytesIO

from .forms import CreateOrderForm
from user_cart.cart_config import UserCart
from .models import Order, OrderItem

from xhtml2pdf import pisa
# Create your views here.

def create_order(request):
    cart = UserCart(request)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], unit_price=item['price'] )
            cart.clear_cart()
            subject = f'Order nr. {order.id}'
            message = f'Dear {order.first_name},\n\n' \
                    f'You have successfully placed an order.' \
                    f'Your order ID is {order.id}.'
            mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
            request.session['order_id'] = order.id
            print('passed:', 'session created')
            return redirect(reverse('payment:process'))
    else:
        form = CreateOrderForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})




def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = 'orders/order/pdf.html'
    context = {'order': order}
    response = render_to_pdf(template, context)
    if response.status_code == 404:
        raise Http404("Invoice not found")
    filename = f"Invoice_{order.id}.pdf"
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response


