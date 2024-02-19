from django.urls import path
from .views import AddToCartView, DeleteFromCartView, PaymentConfirmationView, UpdateCartItemView, ApplyDiscountView

app_name = 'cart'
urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    # path('cart/delete/', DeleteFromCartView.as_view(), name='delete_item'),
    path('cart/delete/<int:product_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('registration/', PaymentConfirmationView.as_view(), name='order_registration'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/apply-discount/', ApplyDiscountView.as_view(), name='apply_discount'),
]
