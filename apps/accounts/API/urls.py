from django.urls import path, include
from .views import OrderListAPIView, AddressCRUDViewSet
from rest_framework.routers import DefaultRouter

app_name = 'panel'

router = DefaultRouter()
router.register(r'addresses', AddressCRUDViewSet, basename='address')

urlpatterns = [
    path('order-history/', OrderListAPIView.as_view(), name='order_history'),
    path('', include(router.urls)),
]
