from django.db import models
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields
# Create your models here.

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=250),
        slug = models.SlugField()
    )
    class Meta:
        # ordering = ['name']
        # indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])
    
    
class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=250),
        slug = models.SlugField(),
        description = models.TextField(),
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    rating = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def __str__(self):
        return str(self.name)
    

