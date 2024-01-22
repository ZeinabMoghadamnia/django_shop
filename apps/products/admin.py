from django.contrib import admin
from .models import Category, Product, Discount, Image, Comment, Like, Brand

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['discounted_price']
    list_display = ('id', 'name', 'category', 'brand', 'quantity', 'price', 'discounted_price', 'is_deleted')
    fieldsets = [
        ('Product Information', {
            'fields': (tuple([
                'name', 'category', 'brand', 'quantity',
            ]),),
        }),
        ('Additional Information', {
            'fields': (tuple([
                'slug', 'description',
            ]),),
        }),
        ('Price Information', {
            'fields': (tuple([
                'price', 'discount', 'discounted_price',
            ]),),
        }),
        ('Status Information', {
            'fields': (tuple([
                'is_active', 'is_deleted',
            ]),),
        }),
    ]
    search_fields = ('name', 'brand', 'category')
    prepopulated_fields = {'slug': ('name',)}

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount_type', 'value', 'activate_at', 'deactivate_at',)
    fieldsets = [
        ('Discount Information', {
            'fields': (tuple([
                'code', 'discount_type', 'value',
            ]),),
        }),
        ('Activate Information', {
            'fields': (tuple([
                'activate_at', 'deactivate_at',
            ]),),
        }),
        ('Status Information', {
            'fields': (tuple([
                'is_active', 'is_deleted',
            ]),),
        }),
    ]
    search_fields = ('code', 'discount_type', 'value')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'is_deleted')
    search_fields = ("name",)
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('id',)
    filter_horizontal = ()
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Information', {'fields': ('name', 'slug', 'image',)}),)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'context', 'author', 'product_id', 'created_at', 'updated_at')
    search_fields = ("author", "context", "product_id")


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'is_main')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Like, LikeAdmin)
