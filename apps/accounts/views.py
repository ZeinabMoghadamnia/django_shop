from django.views.generic import TemplateView, ListView, DetailView
from ..accounts.forms import LoginForm, CustomUserCreationForm, OTPForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy

from django.core.mail import send_mail
import random
import redis
from django.views import View
from django.shortcuts import render, redirect


# from .models import
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    def get_success_url(self):
        return reverse_lazy('products:home')
    def form_valid(self, form):
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('products:home')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submissions (e.g., display errors)
        return self.render_to_response(self.get_context_data(form=form))




class OTPFormView(FormView):
    template_name = 'accounts/otp_form.html'
    form_class = OTPForm
    success_url = '/check_otp/'

    def form_valid(self, form):
        otp = random.randint(1000, 9999)
        email = form.cleaned_data['email']
        send_mail('کد OTP', f'کد OTP شما: {otp}', 'your@example.com', [email])

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.setex(email, 120, otp)  # تغییر در زمان اعتبار

        return super().form_valid(form)


class OTPCheckView(View):
    template_name = 'otp_check.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        otp_entered = request.POST.get('otp')

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        stored_otp = r.get(email)

        if stored_otp and int(otp_entered) == int(stored_otp):
            return redirect('/dashboard/')
        else:
            return render(request, self.template_name, {'error_message': 'کد OTP اشتباه است.'})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('cafemenu:home')
#     else:
#         form = LoginForm()
#
#     return render(request, 'accounts/login.html', {'form': form})