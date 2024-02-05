from django.urls import path
from django_shop.apps.orders.API.views import AddToCartView

app_name = 'orders'
urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
]
