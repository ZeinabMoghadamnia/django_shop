from django.db import models
from ..accounts.models import User
from ..core.models import BaseModel
from django.core.exceptions import ValidationError
# Create your models here.


from django.db import models

class Discount(BaseModel):
    DISCOUNT_TYPES = (
        ('percentage', 'درصدی'),
        ('amount', 'هزینه ای'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

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

# class Discount(BaseModel):
#     title = models.CharField(max_length=50)
#     # costumer =
#     # discount_type = models.CharField(max_length=)
#     discount_code = models.CharField(max_length=6)
#     # amount = models.IntegerField()
#     # def clean(self):
#     #     if self.amount>100:
#     #         raise ValidationError({'amount': ('must be less than 100')})

class Category(BaseModel):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories/', null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='')

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
    # brand = models.ForeignKey()
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, related_name='discounts')
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ['name']

    def like_count(self):
        return self.likes.count()

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
