from django.db import models
from ..core.models import BaseModel
from ..accounts.models import User
from ..products.models import Product
from django.utils.translation import gettext_lazy as _


# Create your models here.

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('price'))
    class Meta:
        verbose_name_plural = _('order items')

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('user'))
    items = models.ForeignKey(OrderItem, on_delete=models.PROTECT, related_name='orders', verbose_name=_('items'))
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('total price'))
    class Meta:
        verbose_name_plural = _('order')

# class Order(BaseModel):
#     customer = models.ForeignKey(Member, on_delete=models.CASCADE)  # Customer باید با مدل مشتری شما جایگزین شود
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت کل سفارش
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
