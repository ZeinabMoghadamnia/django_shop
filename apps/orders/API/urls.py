from django.urls import path
from .views import AddToCartView, ShoppingCartView, DeleteFromCartView

app_name = 'cart'
urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/delete/', DeleteFromCartView.as_view(), name='delete_item'),
]
