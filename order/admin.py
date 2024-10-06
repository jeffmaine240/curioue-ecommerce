from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import OrderItem, Order

# Register your models here.
def export_to_csv(modeladmin, request, queryset):
    ...

def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href={url} >pdf</a>')
order_pdf.short_description = 'invoice'

def order_detail(obj):
    url = reverse('order:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href={url} > view </a>')

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href={url} target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
order_payment.short_description = 'stripe payment'

class OrderItemInline(admin.TabularInline):
    '''Tabular Inline View for OrderItem'''
    model = OrderItem
    raw_id_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','address', 'postal_code', 'created', 'updated', 'paid', order_payment, order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated'] 
    inlines = [OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)