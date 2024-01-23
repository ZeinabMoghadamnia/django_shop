from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView, CategoryListView

app_name = 'products'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='details'),
    path('product/<slug:slug>/like/', ProductDetailView.as_view(), name='like'),
    path('categories/', CategoryListView.as_view(), name='categories'),

]
