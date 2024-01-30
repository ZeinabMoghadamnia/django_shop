from ..accounts.forms import LoginForm, CustomUserCreationForm, OTPForm
from .models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import OTPForm, VerifyOTPForm
from .tasks import send_otp_email_task
from config.redis import OTPRedis
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import random
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

class SendOTPCodeView(View):
    template_name = 'accounts/otp_form.html'
    form_class = OTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                subject = 'Login Code'
                message = str(random.randint(10000, 99999))
                OTPRedis.set_redis(email, message)
                send_otp_email_task.delay(subject, message, email)
                request.session['otp_email'] = email
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'لطفاً ابتدا ثبت نام کنید.')
                return render(request, self.template_name, {'form': form})

        return redirect('accounts:verify_otp')


class VerifyOTPView(View):
    template_name = 'accounts/verify_otp.html'
    form_class = VerifyOTPForm  # تغییر به نام فرم تایید OTP شما

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = request.session.get('otp_email', None)
            if email:
                saved_otp = OTPRedis.get_redis(email).decode('utf-8', 'ignore')
                entered_otp = form.cleaned_data['otp']
                user = authenticate(request, email=email)

                if entered_otp == saved_otp:
                    login(request, user)
                    OTPRedis.delete_redis(email)

                    messages.success(request, 'ورود موفقیت آمیز بود.')
                    return redirect('products:home')
                else:
                    messages.error(request, 'کد وارد شده صحیح نیست.')
            else:
                messages.error(request, 'خطایی رخ داده است. لطفا دوباره تلاش کنید.')

        return render(request, self.template_name, {'form': form})


# def index(request):
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             message = request.POST['message']
#             email = request.POST['email']
#             name = request.POST['name']
#             send_mail("Verify Code",
#                       message,
#                       'settings.EMAIL_HOST_USER',
#                       [email],
#                       fail_silently=False)
#     return render(request,'accounts/otp_form.html')


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

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
