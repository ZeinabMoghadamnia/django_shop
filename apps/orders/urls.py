from django.urls import path, include
from .views import SelectAddressView
from .API.views import ShoppingCartView


# from django_shop.apps.orders.i.ApiView import AddToCartView

app_name = 'orders'
urlpatterns = [
    path('', include("apps.orders.API.urls")),
    path('cart/show/', ShoppingCartView.as_view(), name='cart'),
    path('select-address/', SelectAddressView.as_view(), name='select_address'),
    # path('save-order/', SaveOrderView.as_view(), name='save_order'),
]
