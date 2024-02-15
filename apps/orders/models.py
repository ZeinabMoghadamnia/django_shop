from django.db import models
from ..core.models import BaseModel
from ..products.models import Discount

from ..accounts.models import User
# from apps.accounts
# from django_shop.apps.accounts.models import User
# from accounts.models import User
# from apps.accounts.models import User
# from .apps.accounts.models import User
# from .accounts.models import User



from ..products.models import Product
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Order(BaseModel):
    ORDER_STATUS = (
        ('processing', 'در حال پردازش'),
        ('delivered', 'ارسال شده'),
        ('cancelled', 'لغو شده'),
        ('returned', 'بازگردانده شده'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order', verbose_name=_('user'))
    total_price = models.PositiveIntegerField(verbose_name=_('total price'))
    discounted_total_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('discounted total price'))
    status = models.CharField(choices=ORDER_STATUS, max_length=15, default='processing', verbose_name=_('order status'))
    is_paid = models.BooleanField(default=False, verbose_name=_('payment status'))
    address = models.TextField(verbose_name=_('address'))
    class Meta:
        verbose_name_plural = _('order')

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders', verbose_name=_('orders'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('discount'))

    class Meta:
        verbose_name_plural = _('order items')

# class Order(BaseModel):
#     customer = models.ForeignKey(Member, on_delete=models.CASCADE)  # Customer باید با مدل مشتری شما جایگزین شود
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت کل سفارش
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
