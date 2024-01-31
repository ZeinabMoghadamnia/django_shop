from django.contrib import admin
from admin_extra_buttons.api import button, link
from .models import User, Profile, Address
from ..core.admin import ButtonMixin, CustomExtraButtonsMixin
from .permissions import AccountsAdminPanelPermission


# Register your models here.

class AddressInline(admin.TabularInline):
    model = Address
    fieldsets = [(
        (None, {'fields': ('user', 'province', 'city', 'complete_address')})
    ), ]
    readonly_fields = ['user']
    extra = 0


@admin.register(User)
class UsersAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'phone_number',
        'is_active', 'is_superuser', 'user_type', 'last_login', 'change_button', 'delete_button')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        ('Name', {
            'fields': (tuple(['first_name', 'last_name']),),
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
    list_filter = ('is_superuser', 'user_type', 'is_active', 'is_deleted',)
    inlines = [AddressInline]
    readonly_fields = ('last_login',)

    def get_list_display(self, request):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'operator'):
            return super().get_list_display(request)
        else:
            return ('id', 'first_name', 'last_name', 'email', 'phone_number',
                    'is_active', 'is_superuser', 'user_type', 'last_login', 'show_button')


@admin.register(Profile)
class ProfileAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'img_preview', 'gender', 'date_of_birth', 'user', 'change_button', 'delete_button')
    search_fields = ('date_of_birth', 'gender')
    fieldsets = (('Additional Information', {
        'fields': (tuple(['user', 'date_of_birth', 'gender', 'image']),),
    }),)
    ordering = ('date_of_birth',)
    list_filter = ('gender', 'is_active', 'is_deleted',)

    def get_list_display(self, request):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'operator'):
            return super().get_list_display(request)
        else:
            return ('id', 'img_preview', 'gender', 'date_of_birth', 'user', 'show_button')

@admin.register(Address)
class AddressAdmin(AccountsAdminPanelPermission, CustomExtraButtonsMixin, ButtonMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'province', 'city', 'postal_code', 'is_deleted', 'change_button', 'delete_button')
    search_fields = ('province', 'city', 'complete_address', 'postal_code')
    list_filter = ('province', 'city', 'is_active', 'is_deleted',)

    @link(href=None,
          change_list=False,
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.city}' on Google"
        button.href = f"https://www.google.com/?q={original.city}"

    def get_list_display(self, request):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'operator'):
            return super().get_list_display(request)
        else:
            return ('id', 'user', 'province', 'city', 'postal_code', 'is_deleted', 'show_button')

# admin.site.register(User, UsersAdmin)
# admin.site.register(Address, AddressAdmin)
