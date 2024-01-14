from django.db import models
from ..accounts.models import User
from ..core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Discount(BaseModel):
    DISCOUNT_TYPES = (
        ('percentage', 'Percent'),
        ('amount', 'Amount'),
    )

    code = models.CharField(max_length=50, unique=True, verbose_name=_('discount code'))
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, verbose_name=_('discount type'))
    value = models.PositiveIntegerField(verbose_name=_('value'))
    def clean(self):
        if self.discount_type=='percentage' and self.value > 100:
            raise ValidationError('must be between 0 and 100')

    def __str__(self):
        return self.code


class BaseGrouping(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    category_image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name=_('image'))
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('discount'))
    slug = models.SlugField(unique=True, max_length=20, verbose_name=_('slug'))
    class Meta:
        abstract = True

class Category(BaseGrouping):
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('parent category'))
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"category: {self.name}"

class Brand(BaseGrouping):
    def __str__(self):
        return f"brand: {self.name}"

class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    main_image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name=_('image'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories', verbose_name=_('category'))
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, related_name='discounts', null=True, blank=True, verbose_name=_('discount'))
    discounted_price = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('discounted price'))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brands', verbose_name=_('brand'))
    slug = models.SlugField(unique=True, max_length=20, verbose_name=_('slug'))
    class Meta:
        ordering = ['name']

    def like_count(self):
        return self.likes.count()

@receiver(post_save, sender=Product)
def calculate_discounted_price(sender, instance, **kwargs):
    if hasattr(instance, 'discount') and instance.discount:
        if instance.discount.discount_type in ['percentage', 'amount']:
            if instance.discount.discount_type == 'percentage':
                instance.discounted_price = instance.price - ((instance.discount.value / 100) * instance.price)
            elif instance.discount.discount_type == 'amount':
                instance.discounted_price = instance.price - int(instance.discount.value)
    else:
        instance.discounted_price = None

    if hasattr(instance, 'category') and instance.category and hasattr(instance.category, 'discount') and instance.category.discount:
        if instance.category.discount.discount_type in ['percentage', 'amount']:
            if instance.category.discount.discount_type == 'percentage':
                instance.discounted_price = instance.price - ((instance.category.discount.value / 100) * instance.price)
            elif instance.category.discount.discount_type == 'amount':
                instance.discounted_price = instance.price - int(instance.category.discount.value)
    else:
        instance.discounted_price = None

    instance.save(update_fields=['discounted_price'])


# @receiver(pre_save, sender=Product)
# def calculate_discounted_price(sender, instance, **kwargs):
#     # Disconnect the post_save signal temporarily to avoid recursion
#     post_save.disconnect(calculate_discounted_price, sender=Product, dispatch_uid='calculate_discounted_price')
#
#     if hasattr(instance, 'discount') and instance.discount:
#         if instance.discount.discount_type in ['percentage', 'amount']:
#             if instance.discount.discount_type == 'percentage':
#                 instance.discounted_price = instance.price - ((instance.discount.value / 100) * instance.price)
#             elif instance.discount.discount_type == 'amount':
#                 instance.discounted_price = instance.price - int(instance.discount.value)
#     else:
#         instance.discounted_price = None
#
#     if hasattr(instance, 'category') and instance.category and hasattr(instance.category, 'discount') and instance.category.discount:
#         if instance.category.discount.discount_type in ['percentage', 'amount']:
#             if instance.category.discount.discount_type == 'percentage':
#                 instance.discounted_price = instance.price - ((instance.category.discount.value / 100) * instance.price)
#             elif instance.category.discount.discount_type == 'amount':
#                 instance.discounted_price = instance.price - int(instance.category.discount.value)
#     else:
#         instance.discounted_price = None
#
#     # Reconnect the post_save signal
#     post_save.connect(calculate_discounted_price, sender=Product, dispatch_uid='calculate_discounted_price')

# Connect the post_save signal initially
# post_save.connect(calculate_discounted_price, sender=Product, dispatch_uid='calculate_discounted_price')



class Image(BaseModel):
    sub_image = models.ImageField(upload_to='products/', height_field=None, width_field=None, null=True, blank=True, verbose_name=_('gallery'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image', verbose_name=_('product'))

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', verbose_name=_('reply'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authors', verbose_name=_('author'))
    context = models.TextField(verbose_name=_('content'))
    class Meta:
        ordering = ['create_at']

class Like(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name=_('product'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_who_liked', verbose_name=_('user'))
