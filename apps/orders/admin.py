from django.contrib import admin
from .models import Order, OrderItem
from ..core.admin import ButtonMixin, CustomExtraButtonsMixin
from ..accounts.permissions import AccountsAdminPanelPermission

# Register your models here.

@admin.register(Order)
class OrderAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'is_paid', 'change_button', 'delete_button')
    list_filter = ('is_paid',)

@admin.register(OrderItem)
class OrderItemAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id',)
