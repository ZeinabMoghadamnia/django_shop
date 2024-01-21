from django.urls import path
from .views import HomeView, ProductListView, CategoryListView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('categories/', CategoryListView.as_view(), name='products'),

]
