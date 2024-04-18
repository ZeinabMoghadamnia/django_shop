
class ProductAdminPanelPermission:
    def has_change_permission(self, request, obj=None):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'manager'):
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'manager'):
            return True
        else:
            return False
    def has_add_permission(self, request, obj=None):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'manager'):
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        staff_groups = request.user.groups.values_list('name', flat=True)
        staff_type = request.user.user_type
        is_superuser = request.user.is_superuser
        if is_superuser or (staff_type == 'manager') or (staff_type == 'supervisor'):
            return True
        else:
            return False
