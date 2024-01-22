from django.contrib import admin
from .models import User, Address


# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'username', 'first_name', 'last_name', 'gender', 'email', 'phone_number', 'date_of_birth', 'created_at',
    'is_active', 'is_superuser', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        ('Name', {
            'fields': (tuple(['first_name', 'last_name', 'username']),),
        }),
        ('Group and User Type', {
            'fields': ('groups', 'user_type')
        }),
        ('Administrative Information', {
            'fields': (tuple(['is_superuser', 'is_staff', 'is_active']),),
        }),
        (None, {
            'fields': (tuple(['address', 'last_login']),),
        }),
        ('Contact Information', {
            'fields': (tuple(['email', 'phone_number']),),
        }),
        ('Additional Information', {
            'fields': (tuple(['date_of_birth', 'gender', 'image']),),
        }),
    )
    ordering = ('email',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'province', 'city', 'complete_address', 'postal_code', 'is_deleted')
    search_fields = ('province', 'city', 'complete_address', 'postal_code')


admin.site.register(User, UsersAdmin)
admin.site.register(Address, AddressAdmin)
