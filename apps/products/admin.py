from django.contrib import admin
from .models import Category, Product, Discount, Image, Comment, Like, Brand

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('discounted_price',)

admin.site.register([Category, Discount, Image, Comment, Like, Brand])
admin.site.register(Product, ProductAdmin)

# admin.site.register([Category, Discount, Image, Comment, Like, Brand, Product])