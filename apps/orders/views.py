import json
from .models import Order
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, DetailView
from ..accounts.models import User

# Create your views here.

class CustomerPanelView(DetailView):
    template_name = "orders/panel.html"
    context_object_name = "users"
    model = User

    def get_object(self, queryset=None):
        user_email = self.kwargs.get('email')
        user = get_object_or_404(User, email=user_email)
        order = Order.objects.filter(user=user).first()
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object().user
        context['user'] = user
        context['orders'] = Order.objects.filter(user=user)
        return context


