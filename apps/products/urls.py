from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView, CategoryDetailView, CategoryListView, ProductLikeView, \
    ProductSearchView

app_name = 'products'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='details'),
    path('product/<int:pk>/like/', ProductLikeView.as_view(), name='product_like'),
    path('category/', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_details'),
    path('search/', ProductSearchView.as_view(), name='product_search'),

]
