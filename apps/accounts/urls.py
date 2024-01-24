from django.urls import path
from .views import CustomLoginView, RegisterView, CustomLogoutView, OTPFormView, OTPCheckView

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send_otp/', OTPFormView.as_view(), name='send_otp'),
    path('check_otp/', OTPCheckView.as_view(), name='check_otp'),

]
