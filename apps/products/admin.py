from django.contrib import admin
from .models import Category, Product, Discount, Image, Comment, Like

# Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     readonly_fields = ('discounted_price',)

admin.site.register([Category, Discount, Image, Comment, Like, Product])
# admin.site.register(Product, ProductAdmin)
