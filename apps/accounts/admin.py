from django.contrib import admin
from .models import User, Profile, Address


# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'created_at',
    'is_active', 'is_superuser', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        ('Name', {
            'fields': (tuple(['first_name', 'last_name', 'username', 'image']),),
        }),
        ('Contact Information', {
            'fields': (tuple(['email', 'phone_number']),),
        }),
        ('Administrative Information', {
            'fields': (tuple(['is_superuser', 'is_staff', 'is_active']),),
        }),
        ('Details Information', {
            'fields': ('last_login',),
        }),
        ('Group and User Type', {
            'fields': ('groups', 'user_type'),
        }),
    )
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['gender', 'date_of_birth']
    search_fields = ('date_of_birth', 'gender')
    fieldsets = (('Additional Information', {
            'fields': (tuple(['date_of_birth', 'gender', 'image']),),
        }),)
    ordering = ('birthdate',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'province', 'city', 'postal_code', 'is_deleted')
    search_fields = ('province', 'city', 'complete_address', 'postal_code')


admin.site.register(User, UsersAdmin)
admin.site.register(Address, AddressAdmin)
