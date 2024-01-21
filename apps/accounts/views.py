from django.views.generic import TemplateView, ListView, DetailView
from ..accounts.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy

# from .models import
# Create your views here.

from django.contrib.auth.views import LoginView
from .forms import LoginForm  # Import your LoginForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Specify the path to your login template
    form_class = LoginForm  # Set the form class to your LoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        # Your additional logic after a successful login (if needed)
        return response

    def get_success_url(self):
        # Define the URL to redirect to after successful login
        return 'cafemenu:home'

class LogoutPageView(LogoutView):
    success_url = reverse_lazy('home')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        return super().form_valid(form)


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