from django.db import models
from ..core.models import BaseModel
from ..accounts.models import User
from ..products.models import Product


# Create your models here.

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    items = models.ForeignKey(OrderItem, on_delete=models.PROTECT, related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

# class Order(BaseModel):
#     customer = models.ForeignKey(Member, on_delete=models.CASCADE)  # Customer باید با مدل مشتری شما جایگزین شود
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت کل سفارش
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
