from django.contrib import admin
from parler.admin import TranslatableAdmin

# Register your models here.
from .models import Category, Product

class CategoryAdmin(TranslatableAdmin):
    list_display = ['id', 'name', 'slug']
    # prepopulated_fields = {'slug':['name']}
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'created', 'availability']
    list_filter = ['availability', 'created', 'updated']
    list_editable = ['price', 'availability']
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

# python manage.py makemigrations shop --name "translations"
