from django.contrib import admin
from .models import Category, Product, Discount, Image, Comment, Like, Brand
from ..core.admin import ButtonMixin, CustomExtraButtonsMixin
from admin_extra_buttons.api import button, link
from django.utils.html import mark_safe, format_html

# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Product)
class ProductAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    readonly_fields = ['discounted_price']
    list_display = ('id', 'display_main_image', 'name', 'category', 'brand', 'quantity', 'price', 'discounted_price', 'is_deleted', 'change_button', 'delete_button')
    inlines = [ImageInline]
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
    list_filter = ('category', 'brand', 'is_deleted', 'is_active',)

    def display_main_image(self, obj):
        main_image = obj.image.filter(is_main=True).first()
        if main_image:
            return format_html('<img src="{}" width="auto" height="100" />'.format(main_image.sub_image.url))
        return None

    def display_comment(self, obj):
        comment = obj.comments.filter(is_main=True).first()
        if comment:
            return format_html('<img src="{}" width="auto" height="100" />'.format(main_image.sub_image.url))
        return None

    display_main_image.short_description = 'Main Image'

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"

@admin.register(Discount)
class DiscountAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'code', 'discount_type', 'value', 'activate_at', 'deactivate_at', 'change_button', 'delete_button')
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
    list_filter = ('discount_type', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.code}' on Google"
        button.href = f"https://www.google.com/?q={original.code}"

@admin.register(Category)
class CategoryAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'is_deleted', 'change_button', 'delete_button')
    search_fields = ("name",)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"

@admin.register(Brand)
class BrandAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'change_button', 'delete_button')
    search_fields = ('name',)
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Information', {'fields': ('name', 'slug', 'image',)}),)
    list_filter = ('name', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"

@admin.register(Comment)
class CommentAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'context', 'author', 'product_id', 'created_at', 'updated_at', 'change_button', 'delete_button')
    search_fields = ("author", "context", "product_id")
    list_filter = ('product_id', 'author', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.product}' on Google"
        button.href = f"https://www.google.com/?q={original.product}"

@admin.register(Image)
class ImageAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'img_preview', 'product', 'is_main', 'change_button', 'delete_button')
    list_filter = ('product', 'is_main', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.product}' on Google"
        button.href = f"https://www.google.com/?q={original.product}"

@admin.register(Like)
class LikeAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'change_button', 'delete_button')
    list_filter = ('product', 'user', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.product}' on Google"
        button.href = f"https://www.google.com/?q={original.product}"

