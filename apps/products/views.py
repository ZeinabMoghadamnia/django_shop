from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category, Like
from django.http import JsonResponse
# Create your views here.

class HomeView(ListView):

    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image').order_by('id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()

# views.py
# views.py
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Category, Product

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Category

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        subcategories = category.filter(parent=self.get_object())
        products = category.products.all()
        context['subcategories'] = subcategories
        context['products'] = products
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['item_name'] = self.object
        description_lines = self.object.description.splitlines()
        context['description_lines'] = description_lines
        context['item_images'] = self.object.image.all()
        context['similar_item'] = Product.objects.filter(category=self.object.category)
        # context['add_to_cart_form'] = AddToCartProductForm()
        context['comments'] = self.object.comments.filter(reply__isnull=True)
        context['like_count'] = self.object.likes.count()

        return context
