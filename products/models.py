from django.db import models
from ..core.models import BaseModel
# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=50)
    sub_category = models.ForeignKey('self', on_delete=models, null=True, blank=True)
    category_image = models.ImageField(upload_to='')
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.category_name


class Product(BaseModel):
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_quantity = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='')
    product_category = models.ForeignKey(Category, on_delete=models, related_name='product_category', null=True, blank=True)
    # product_brand = models.ForeignKey()

