from django.contrib import admin
from .models import Order, OrderItem
from ..core.admin import ButtonMixin, CustomExtraButtonsMixin
from ..accounts.permissions import AccountsAdminPanelPermission
from admin_extra_buttons.api import button, link
from django.utils.html import mark_safe, format_html


# Register your models here.

@admin.register(Order)
class OrderAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'total_price', 'discounted_total_price', 'is_paid', 'change_button', 'delete_button')
    list_filter = ('is_paid',)

    # @link(href=None,
    #       change_list=False,
    #       html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    # def search_on_google(self, button):
    #     original = button.context['original']
    #     button.label = f"Search '{original.items.name}' on Google"
    #     button.href = f"https://www.google.com/?q={original.items.name}"

@admin.register(OrderItem)
class OrderItemAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'discount', 'is_active', 'is_deleted', 'change_button', 'delete_button')
    list_filter = ('product', 'is_deleted', 'is_active',)
    def display_main_image(self, obj):
        main_image = obj.image.filter(is_main=True).first()
        if main_image:
            return format_html('<img src="{}" width="auto" height="100" />'.format(main_image.sub_image.url))
        return None

    display_main_image.short_description = 'Main Image'

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.product.name}' on Google"
        button.href = f"https://www.google.com/?q={original.product.name}"

