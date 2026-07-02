from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from items.models import LostItem, FoundItem
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('items:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CampusConnect, {user.first_name}! Your account is ready.")
            return redirect('items:dashboard')
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CampusLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().first_name}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. See you soon!")
    return redirect('items:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    my_lost = LostItem.objects.filter(owner=request.user).order_by('-created_at')
    my_found = FoundItem.objects.filter(finder=request.user).order_by('-created_at')

    context = {
        'form': form,
        'my_lost': my_lost,
        'my_found': my_found,
        'lost_count': my_lost.count(),
        'found_count': my_found.count(),
        'returned_count': my_lost.filter(status='returned').count() + my_found.filter(status='returned').count(),
    }
    return render(request, 'accounts/profile.html', context)
