from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register_view(request):
    if request.user.is_authenticated:
        # 👇 Redirect logged-in users to their respective pages
        if getattr(request.user, 'role', '') == 'admin':
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '✅ Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, f'Something went wrong: {form.errors}')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # 👇 Redirect logged-in users away from login page
        if (
            request.user.is_superuser or
            request.user.is_staff or
            getattr(request.user, 'role', '') == 'admin'
        ):

            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser  or user.is_staff or getattr(user, 'role', '') == 'admin':
                messages.success(request, f'Welcome back Admin {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.success(request, f'Welcome {user.username}!')
                return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password')
    return render(request, 'accounts/login.html')



@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out successfully.")
    return redirect('login')
