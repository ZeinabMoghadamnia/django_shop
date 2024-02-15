from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    سفارشی برای بررسی اینکه آیا کاربر مالک آبجکت است یا خیر.
    """

    def has_object_permission(self, request, view, obj):
        # اجازه خواندن را به همه می‌دهد
        if request.method in permissions.SAFE_METHODS:
            return True

        # مجوز‌های دیگر را تنها به مالک می‌دهد
        return obj.user == request.user