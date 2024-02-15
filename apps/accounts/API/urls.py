from django.urls import path, include
from .views import OrderListAPIView, OrderItemListAPIView, AddressCreateView, AddressDetailView, AddressListView, PanelView
from rest_framework.routers import DefaultRouter

app_name = 'panel'

# router = DefaultRouter()
# router.register(r'addresses', AddressCRUDViewSet, basename='address')

urlpatterns = [
    path('', PanelView.as_view(), name='user_panel'),
    path('order-history/', OrderListAPIView.as_view(), name='order_history'),
    path('order-detail/<int:order_id>/', OrderItemListAPIView.as_view(), name='order_detail'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    # path('', include(router.urls)),
]
