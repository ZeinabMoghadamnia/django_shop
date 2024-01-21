from django.urls import path
from .views import HomeView, ProductListView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products', ProductListView.as_view(), name='products'),

]
