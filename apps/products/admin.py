from django.contrib import admin
from .models import Category, Product, Discount, Image, Comment, Like, Brand

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['discounted_price']
    list_display = ('id', 'name', 'category', 'brand', 'quantity', 'price', 'discounted_price', 'is_deleted')
    search_fields = ("name", "brand")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'is_deleted')
    search_fields = ("name",)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('id',)
    filter_horizontal = ()
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Main', {'fields': ('name', 'slug', 'image',)}),)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'context', 'author', 'product_id', 'created_at', 'updated_at')
    search_fields = ("title", "description")


class ImageAdmin(admin.ModelAdmin):
    # readonly_fields = ['img_preview']
    list_display = ('id', 'product', 'is_main')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'discount_type', 'value')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Discount, DiscountAdmin)