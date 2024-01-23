from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView, CategoryDetailView, CategoryListView

app_name = 'products'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='details'),
    # path('product/<slug:slug>/like/', ProductDetailView.as_view(), name='like'),
    path('category/', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_details'),

]
