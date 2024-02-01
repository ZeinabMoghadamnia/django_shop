from django.db import models
from ..accounts.models import User
from ..core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.contrib import messages

# Create your models here.

class Discount(BaseModel):
    DISCOUNT_TYPES = (
        ('percentage', 'Percent'),
        ('amount', 'Amount'),
    )

    code = models.CharField(max_length=50, unique=True, verbose_name=_('discount code'))
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, verbose_name=_('discount type'))
    value = models.PositiveIntegerField(verbose_name=_('value'))
    activate_at = models.DateTimeField(verbose_name=_('activation date'))
    deactivate_at = models.DateTimeField(verbose_name=_('deactivation date'))
    class Meta:
        verbose_name_plural = _('discount code')

    def clean(self):
        if self.discount_type=='percentage' and not MinValueValidator(0) and not MaxValueValidator(100):
            raise ValidationError('must be between 0 and 100')
        if self.discount_type=='amount' and not MinValueValidator(0) and not MaxValueValidator(self.value):
            raise ValidationError('must be between 0 and price')

    def __str__(self):
        return self.code


class BaseOfGrouping(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('discount'))
    slug = models.SlugField(unique=True, max_length=20, blank=True, null=True, verbose_name=_('slug'))
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Brand(BaseOfGrouping):
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    image = models.ImageField(upload_to='brands/', null=True, blank=True, verbose_name=_('image'))
    class Meta:
        verbose_name_plural = _('brand')
    def __str__(self):
        return self.name

class Category(BaseOfGrouping):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('parent category'))
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name=_('image'))
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories', verbose_name=_('category'))
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, related_name='discounts', null=True, blank=True, verbose_name=_('discount'))
    discounted_price = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('discounted price'))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brands', verbose_name=_('brand'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=20, verbose_name=_('slug'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('product')

    def __str__(self):
        return self.name

    def img_preview(self):
        main_image = self.images.filter(is_main=True).first()
        return mark_safe('<img src="/media/%s" width="auto" height="100" />' % (self.sub_image))

    # def number_of_likes(self):
    #     return self.likes.count()


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1

            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)





class Image(BaseModel):
    sub_image = models.ImageField(upload_to='products/', height_field=None, width_field=None, null=True, blank=True, verbose_name=_('images'))
    is_main = models.BooleanField(default=False, verbose_name=_('main image'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image', verbose_name=_('product'))
    class Meta:
        verbose_name_plural = _('image')

    def __str__(self):
        return self.product.name

    def img_preview(self):
        return mark_safe('<img src="/media/%s" width="auto" height="100" />' % (self.sub_image))


class Comment(BaseModel):
    ACCEPT_STATUS = (
        ('approved', 'approved'),
        ('waiting', 'waiting'),
        ('rejected', 'rejected'),
    )
    status = models.CharField(max_length=10, choices=ACCEPT_STATUS, default='waiting', verbose_name=_('verify_status'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True, verbose_name=_('reply'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors', verbose_name=_('author'))
    context = models.TextField(verbose_name=_('content'))
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = _('comments')

    def __str__(self):
        return f"{self.product} : {self.author}"

class Like(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name=_('products'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_liked', verbose_name=_('user'))
    is_liked = models.BooleanField(default=False, verbose_name=_('like status'))

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')

    def toggle_like(self):
        self.is_liked = not self.is_liked
        if not self.is_liked:
            self.delete()
        else:
            self.save()
