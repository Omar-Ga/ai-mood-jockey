from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from playlist_generator.models import MoodQuery

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'web_interface/dashboard.html')
    return render(request, 'web_interface/landing.html') # We can just point this to login or a welcome page. Let's redirect to login for simplicity.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('web_interface:home')
    else:
        form = UserCreationForm()
    return render(request, 'web_interface/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('web_interface:home')
    else:
        form = AuthenticationForm()
    return render(request, 'web_interface/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('web_interface:login')
    # fallback for GET
    logout(request)
    return redirect('web_interface:login')

@login_required
def history_view(request):
    queries = MoodQuery.objects.filter(user=request.user).prefetch_related('tracks').order_by('-created_at')
    return render(request, 'web_interface/history.html', {'queries': queries})
