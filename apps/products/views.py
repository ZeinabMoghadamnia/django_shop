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

class CategoryDetailView(ListView):
    model = Product
    # template_name = 'cafemenu/menuitem_list.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
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

    def post(self, request, *args, **kwargs):
        # بررسی اگر کاربر لاگین کرده باشد
        if request.user.is_authenticated:
            # دریافت نمونه محصول
            product = self.get_object()
            # تغییر وضعیت لایک توسط کاربر
            product.toggle_like(request.user)
            return self.get(request, *args, **kwargs)
        else:
            # اگر کاربر لاگین نکرده باشد، می‌توانید یک پیام خطا نمایش دهید یا به هر شیوه‌ای بخواهید برخورد کنید.
            return HttpResponseForbidden("شما باید لاگین کنید تا بتوانید لایک کنید.")

