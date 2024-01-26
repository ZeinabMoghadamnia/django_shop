from ..accounts.forms import LoginForm, CustomUserCreationForm, OTPForm
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



class SendOTPCodeView(View):
    template_name = 'accounts/otp_form.html'
    form_class = OTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            subject = 'Login Code'
            message = str(random.randint(10000, 99999))
            recipient = form.cleaned_data['email']
            OTPRedis.set_redis(recipient, message)
            send_otp_email_task.delay(subject, message, recipient)

        return redirect('accounts:verify_otp')

class VerifyOTPView(View):
    template_name = 'accounts/verify_otp.html'
    form_class = VerifyOTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('otp_code')
            recipient = OTPRedis.key_by_code(entered_code.decode('utf-8', 'ignore'))
            stored_code_bytes = OTPRedis.get_redis(recipient)

            if stored_code_bytes:
                stored_code = stored_code_bytes.decode('utf-8', 'ignore')
                if entered_code == stored_code:
                    user = authenticate(request, username=recipient, password='')
                    if user:
                        login(request, user)
                        OTPRedis.delete_redis(recipient)
                        return redirect('products:home')

        return render(request, self.template_name, {'form': form, 'error_message': 'Invalid OTP code'})

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



#
# import random
# import redis
# from django.conf import settings
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.serializers import Serializer, CharField
# from africastalking.Africastalking import initialize
# from africastalking.SMS import send
#
# # Initialize Redis client
# redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
#
# # Initialize African Talking API
# initialize(settings.AFRICASTALKING_API_USERNAME, settings.AFRICASTALKING_API_KEY)
#
# class GenerateOTPSerializer(Serializer):
#     phone_number = CharField()
#
# class VerifyOTPSerializer(Serializer):
#     phone_number = CharField()
#     otp = CharField()
#
# class SendOTP(APIView):
#     def post(self, request):
#         serializer = GenerateOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             otp = str(random.randint(1000, 9999))
#             redis_client.setex(phone_number, 300, otp)
#
#             # Send OTP via SMS
#             message = f'Your OTP is: {otp}'
#             recipients = [phone_number]
#             try:
#                 send(message, recipients)
#                 return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class VerifyOTP(APIView):
#     def post(self, request):
#         serializer = VerifyOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             otp = serializer.validated_data['otp']
#
#             # Check if OTP exists in Redis
#             stored_otp = redis_client.get(phone_number)
#             if stored_otp and stored_otp.decode('utf-8') == otp:
#                 # OTP is valid
#                 return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
#             else:
#                 # OTP is invalid
#                 return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#

#
# class OTPFormView(FormView):
#     template_name = 'accounts/otp_form.html'
#     form_class = OTPForm
#     success_url = '/check_otp/'
#
#     def form_valid(self, form):
#         otp = random.randint(1000, 9999)
#         email = form.cleaned_data['email']
#         send_mail('کد OTP', f'کد OTP شما: {otp}', 'your@example.com', [email])
#
#         r = redis.StrictRedis(host='localhost', port=6379, db=0)
#         r.setex(email, 120, otp)  # تغییر در زمان اعتبار
#
#         return super().form_valid(form)
#
#
# class OTPCheckView(View):
#     template_name = 'accounts/verify_otp.html'
#
#     def post(self, request, *args, **kwargs):
#         email = request.POST.get('email')
#         otp_entered = request.POST.get('otp')
#
#         r = redis.StrictRedis(host='localhost', port=6379, db=0)
#         stored_otp = r.get(email)
#
#         if stored_otp and int(otp_entered) == int(stored_otp):
#             return redirect('/dashboard/')
#         else:
#             return render(request, self.template_name, {'error_message': 'کد OTP اشتباه است.'})


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