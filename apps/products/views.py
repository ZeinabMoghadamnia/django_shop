from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category, Like
from django.http import JsonResponse
from .forms import CommentForm


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
    queryset = Category.objects.filter(parent=None).order_by('name')


# views.py

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        subcategories = Category.objects.filter(parent=category)
        if subcategories.exists():
            context['subcategories'] = subcategories
        else:
            context['products'] = Product.objects.filter(category=category)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'details'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        description_lines = self.object.description.splitlines()
        context['description_lines'] = description_lines
        context['item_images'] = self.object.image.all()
        context['similar_item'] = Product.objects.filter(category=self.object.category)
        context['like_count'] = self.object.likes.count()
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.author = self.request.user
            comment.save()
        return redirect('accounts:verify_otp')
