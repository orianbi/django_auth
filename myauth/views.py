from django.http import request
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login, authenticate
from django.views import View
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = 'accounts/login.html'
    next_page = 'login'

class HomeView(View):
    template_name = 'accounts/home.html'

    def get(self, request):
        return render(request, self.template_name)

# def LogoutView(request):
#     logout(request)
#     return redirect(reverse('login'))

class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form':form,})
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user=authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        
        return render(request, self.template_name, {'form':form,})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Password kamu berhasil diubah')
        return super().form_valid(form)