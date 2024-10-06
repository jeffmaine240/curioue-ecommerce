from django.core.mail import EmailMessage
from io import BytesIO
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

import stripe
from xhtml2pdf import pisa

from order.models import Order
from user_cart.cart_config import UserCart

# Using Django
@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, 
      sig_header,
      settings.STRIPE_WEBHOOK_SECRET,
    )
  except ValueError as e:
    return HttpResponse(status=400)

  if event.type == 'checkout.session.completed':
    cart = UserCart(request)
    session = event.data.object 
    print(session)
    if session.mode == 'payment' and session.payment_status == 'paid':
      order = get_object_or_404(Order, id=session.client_reference_id)
      order.paid = True
      order.stripe_id = session.payment_intent
      order.save()
      print
      template = get_template('orders/order/pdf.html')
      context = {'order': order}
      subject = f'My Shop - Invoice no. {order.id}'
      message = 'Please, find attached the invoice for your recent purchase.'
      email = EmailMessage(subject, message, 'admin@myshop.com',[order.email])
      html = template.render(context)
      result = BytesIO()
      pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      if not pdf.err:
          email.attach(f'order_{order.id}.pdf', result.getvalue(), 'application/pdf')
          email.send()
      cart.clear_cart()
  return HttpResponse(status=200)