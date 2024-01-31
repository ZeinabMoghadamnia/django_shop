from ..accounts.forms import LoginForm, CustomUserCreationForm, OTPForm
from .models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
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
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
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

class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.is_active = False
            user.save()

            self.send_activation_email(request, user)

            return redirect('accounts:login')

        return render(request, self.template_name, {'form': form})

    def send_activation_email(self, request, user):

        token = default_token_generator.make_token(user)
        activation_url = request.build_absolute_uri(reverse('accounts:activate', args=[str(token)]))
        subject = 'Activate your account'
        message = f'Click the following link to activate your account:\n\n{activation_url}'
        to_email = user.email

        send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])


class ActivateAccountView(View):
    def get(self, request, token, *args, **kwargs):

        user = self.get_user_by_token(token)

        if user:
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'حساب کاربری شما فعال است')
            else:
                messages.success(request, 'حساب کاربری شما از قبل فعال است')
        else:
            messages.error(request, 'توکن فعالسازی نامعتبر است')

        return redirect('accounts:login')

    def get_user_by_token(self, token):

        try:
            user_id = default_token_generator.check_token(str(token))
            return User.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

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
