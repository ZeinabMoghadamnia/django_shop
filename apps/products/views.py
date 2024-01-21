from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category
# Create your views here.

class HomeView(ListView):

    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image').order_by('id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()
