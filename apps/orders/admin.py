from django.contrib import admin
from .models import Order, OrderItem
from ..core.admin import ButtonMixin, CustomExtraButtonsMixin

# Register your models here.

@admin.register(Order)
class OrderAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'is_paid', 'change_button', 'delete_button')
    list_filter = ('is_paid',)

@admin.register(OrderItem)
class OrderItemAdmin(CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id',)
