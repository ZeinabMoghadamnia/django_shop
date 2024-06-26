from django.urls import path, include
from .views import OrderListAPIView, OrderItemListAPIView, AddressCreateView, AddressListView, \
    PanelView, UserDetailView, ProfileDetailView, AddressDeleteView, AddressEditView, ProfileEditView
from rest_framework.routers import DefaultRouter

app_name = 'panel'

urlpatterns = [
    path('', PanelView.as_view(), name='user_panel'),
    path('order-history/', OrderListAPIView.as_view(), name='order_history'),
    path('order-detail/<int:order_id>/', OrderItemListAPIView.as_view(), name='order_detail'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/delete/<int:address_id>/', AddressDeleteView.as_view(), name='address-delete'),
    path('addresses/edit/<int:address_id>/', AddressEditView.as_view(), name='address-edit'),
    path('user-detail/', UserDetailView.as_view(), name='user_detail'),
    path('profile-detail/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile-edit/<int:user_id>/', ProfileEditView.as_view(), name='profile-edit'),

    # path('', include(router.urls)),
]
# urlpatterns += router.urls
