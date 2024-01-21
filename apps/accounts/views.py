from django.views.generic import TemplateView, ListView, DetailView
from ..accounts.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy

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