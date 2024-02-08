from django.urls import path, include
from .views import CustomerPanelView, SelectAddressView, SaveOrderView
from .API.views import ShoppingCartView


# from django_shop.apps.orders.API.ApiView import AddToCartView

app_name = 'orders'
urlpatterns = [
    path('', include("apps.orders.API.urls")),
    # path('cart/', CartView.as_view(), name='cart'),
    path('cart/show/', ShoppingCartView.as_view(), name='cart'),
    path('panel/<str:email>/', CustomerPanelView.as_view(), name='panel'),
    path('select-address/', SelectAddressView.as_view(), name='select_address'),
    path('save-order/', SaveOrderView.as_view(), name='save_order'),
    # path('panel/<str:email>/<str:token>/', CustomerPanelView.as_view(), name='panel'),
]
