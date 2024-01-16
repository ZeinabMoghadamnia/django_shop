from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
# Create your views here.

class IndexView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image').order_by('id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
