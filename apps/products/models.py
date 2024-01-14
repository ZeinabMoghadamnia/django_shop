from django.db import models
from ..accounts.models import User
from ..core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Discount(BaseModel):
    DISCOUNT_TYPES = (
        ('percentage', 'Percent'),
        ('amount', 'Amount'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.PositiveIntegerField()

    # print("---------------------------------------",discount_type)
    def clean(self):
        if self.discount_type=='percentage' and self.value < 100:
            raise ValidationError({'amount': ('must be less than 100!')})


    # def apply_discount(request, discount_code):
    #     # یافتن تخفیف با استفاده از کد
    #     discount = get_object_or_404(Discount, code=discount_code)
    #
    #     # محاسبه مقدار تخفیف بر اساس نوع تخفیف
    #     if discount.discount_type == 'percentage':
    #         discount_amount = (Decimal(discount.value) / 100) * total_cart_amount
    #     else:
    #         discount_amount = Decimal(discount.value)
    #
    #     # اعمال تخفیف به سبد خرید
    #     total_amount_after_discount = total_cart_amount - discount_amount
    #
    #     # افزودن اطلاعات تخفیف به سشن (مثلاً برای نمایش در صفحه پرداخت)
    #     request.session['discount_details'] = {
    #         'code': discount.code,
    #         'amount': discount_amount,
    #     }
    #
    #     return total_amount_after_discount

    def __str__(self):
        return self.code


class Category(BaseModel):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories/', null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, related_name='discounts')
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    # brand = models.ForeignKey()
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ['name']

    # print("-------------------------------------------------------------",discount.discount_type)

    # @receiver(post_save, sender='products.Product')
    # def calculate_discounted_price(self, sender, instance, **kwargs):
    #     if instance.discount is not None:
    #         if instance.discount.discount_type == 'percentage' or self.category.discount.discount_type == 'percentage':
    #             instance.discounted_price = self.price - ((self.discount.value / 100) * self.price)
    #             # print(self.discounted_price)
    #
    #         elif self.discount.discount_type == 'amount' or self.category.discount.discount_type == 'amount':
    #             self.discounted_price = self.price - int(self.discount.value)

    # @receiver(post_save, sender='products.Product')
    # def post_save_calculate_discounted_price(cls, sender, instance, **kwargs):
    #     instance.calculate_discounted_price()

    # def save(self, *args, **kwargs):
    #     self.calculate_discounted_price()
    #     super(Product, self).save(*args, **kwargs)

    def like_count(self):
        return self.likes.count()

    def clean(self):
        print(self.discount)
@receiver(post_save, sender=Product)
def calculate_discounted_price(sender, instance, **kwargs):
    if instance.discount is not None:
        if instance.discount.discount_type == 'percentage' or instance.category.discount.discount_type == 'percentage':
            instance.discounted_price = instance.price - ((instance.discount.value / 100) * instance.price)

        elif instance.discount.discount_type == 'amount' or instance.category.discount.discount_type == 'amount':
            instance.discounted_price = instance.price - int(instance.discount.value)

# @receiver(post_save, sender='products.Product')
# def post_save_calculate_discounted_price(sender, instance, **kwargs):
#     instance.calculate_discounted_price()

class Image(BaseModel):
    sub_image = models.ImageField('Product_Image', upload_to='products/', height_field=None, width_field=None, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authors')
    context = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['create_at']

class Like(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_who_liked')
