from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
# Create your views here.


class SelectLanguage(TemplateView):
    template_name = 'products/language.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # درخواست زبان انتخابی از کاربر
        language = self.request.GET.get('language', 'fa')  # اگر زبان انتخاب نشده باشد، زبان فارسی را پیش‌فرض قرار دهید

        # تغییر زبان سیستم
        activate(language)

        # دریافت اطلاعات مدل بر اساس زبان
        my_model_data = Product.objects.all()

        context['my_model_data'] = my_model_data
        context['language'] = language

        return context
class ProductListView(ListView):

    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image').order_by('id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
