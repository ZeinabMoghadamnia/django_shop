from django.urls import path
from .views import CustomLoginView, RegisterView, CustomLogoutView, SendOTPCodeView, VerifyOTPView

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send_otp/', SendOTPCodeView.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),

]
