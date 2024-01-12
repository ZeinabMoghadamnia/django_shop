from django.db import models
from ..core.models import BaseModel
# Create your models here.

class Discount(BaseModel):
    discount_id = models.AutoField(primary_key=True)
    discount_choice = (
        ('percent', 'Percent'),
        ('price', 'Price')
    )
    discount_type = models.CharField(max_length=6, choices=discount_choice)
    percentage = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    # category_discount =
class ProductInformatin(BaseModel):
    product_id = models.PositiveIntegerField(primary_key=True)
    product_name = models.CharField(max_length=30)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_inventory = models.PositiveIntegerField()
    product_brand = models.CharField(max_length=50)
    Is_active = models.BooleanField(default=True)
    product_slug = models.SlugField(unique=True)
    product_category = models.ForeignKey(Category, on_delete=models)

