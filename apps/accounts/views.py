from django.views.generic import TemplateView, ListView, DetailView
from ..accounts.forms import LoginForm
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserCreationForm, LoginForm
from django.contrib.auth import login, authenticate, logout


# from .models import
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('cafemenu:home')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})