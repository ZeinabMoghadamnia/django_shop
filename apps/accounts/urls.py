from django.urls import path
from .views import LoginPageView, RegisterView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

]
