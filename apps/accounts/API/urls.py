from django.urls import path, include
from .views import OrderListAPIView, OrderItemListAPIView, AddressCreateView, AddressDetailView, AddressListView, \
    PanelView, UserViewSet, ProfileViewSet, UserDetailView, ProfileDetailView
from rest_framework.routers import DefaultRouter

app_name = 'panel'

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user_info')
# router.register(r'profiles', ProfileViewSet, basename='profile_info')
# router.register(r'user-profile', UserProfileViewSet, basename='user-profile')  # Add this line

urlpatterns = [
    path('', PanelView.as_view(), name='user_panel'),
    path('order-history/', OrderListAPIView.as_view(), name='order_history'),
    path('order-detail/<int:order_id>/', OrderItemListAPIView.as_view(), name='order_detail'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),

    path('user-detail/', UserDetailView.as_view(), name='user_detail'),
    path('profile-detail/', ProfileDetailView.as_view(), name='profile_detail'),
    # path('', include(router.urls)),
]
# urlpatterns += router.urls
