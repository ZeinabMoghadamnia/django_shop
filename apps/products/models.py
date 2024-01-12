from django.db import models
from FinalProject.apps.core.models import BaseModel
# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=50)
    sub_category = models.ForeignKey('self', on_delete=models, null=True, blank=True)
    is_sub_category = models.BooleanField(default=False)
    category_image = models.ImageField(upload_to='')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to='')
    category = models.ForeignKey(Category, on_delete=models, related_name='products')
    brand = models.ForeignKey()
    class Meta:
        ordering = ['name']

    def like_count(self):
        return self.likes.count()

class Image(BaseModel):
    sub_image = models.ImageField('Menu_Item_Image', upload_to='menu_item_img/', height_field=None, width_field=None, null=True, blank=True)

class Discount(BaseModel):
    title = models.CharField(max_length=50)
    # costumer =
    product = models.ForeignKey(Product, on_delete=models)
    discount_type = models.CharField(max_length=)
    discount_code = models.CharField(max_length=6)

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models)
    reply = models.ForeignKey('self', on_delete=models)
    # author = models.ForeignKey()
    context = models.TextField()
    is_reply = models.BooleanField(default=False)
    class Meta:
        ordering = ['create_at']

class Like(BaseModel):
    product = models.ForeignKey(Product, on_delete=models, related_name='likes')
    # user = models.ForeignKey()
