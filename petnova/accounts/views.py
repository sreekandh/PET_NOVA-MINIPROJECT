from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_admin:
                    return redirect('admin_home')
                elif user.is_trainer:
                    return redirect('trainer_home')
                elif user.is_caretaker:
                    return redirect('caretaker_home')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('/accounts/login/')  # Redirect to the custom login page


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html', {'user': request.user})

@login_required
def admin_home(request):
    return render(request, 'admin_fn/admin_home.html')

@login_required
def trainer_home(request):
    return render(request, 'trainer_fn/trainer_home.html')

@login_required
def caretaker_home(request):
    return render(request, 'caretaker_fn/caretaker_home.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

