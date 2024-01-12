from django.db import models
from ..core.models import BaseModel
from ..accounts.models import Member
from ..products.models import Product


# Create your models here.

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Order(BaseModel):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)