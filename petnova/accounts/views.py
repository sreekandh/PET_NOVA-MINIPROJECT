from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from admin_fn.models import Trainer
from .forms import RegistrationForm, LoginForm
from admin_fn.forms import TrainerForm

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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from admin_fn.models import Trainer, Caretaker  # Ensure you import your models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model defined in your project

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Attempt to authenticate with the User model
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Check user roles and redirect accordingly
                if user.is_admin:
                    return redirect('admin_home')
                elif user.is_caretaker:
                    return redirect('caretaker_home')
                else:
                    return redirect('home')
            else:
                # If User authentication fails, check for Trainer
                try:
                    trainer = Trainer.objects.get(email=email)
                    # Direct password comparison (since Trainer passwords are stored in plain text)
                    if trainer.password == password:
                        # Manually create session for Trainer
                        request.session['trainer_id'] = trainer.id
                        request.session['trainer_name'] = trainer.trainer_name
                        request.session['is_trainer'] = True
                        return redirect('trainer_home')
                    else:
                        messages.error(request, 'Invalid email or password.')
                except Trainer.DoesNotExist:
                    # Check for Caretaker authentication
                    try:
                        caretaker = Caretaker.objects.get(email=email)
                        if caretaker.password == password:
                            # Manually create session for Caretaker
                            request.session['caretaker_id'] = caretaker.id
                            request.session['caretaker_name'] = caretaker.caretaker_name
                            request.session['is_caretaker'] = True
                            return redirect('caretaker_home')
                        else:
                            messages.error(request, 'Invalid email or password.')
                    except Caretaker.DoesNotExist:
                        messages.error(request, 'Invalid email or password.')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def trainer_logout(request):
    """Logout the trainer manually by clearing the session."""
    auth_logout(request)  # This will clear the session for the User (if logged in)
    request.session.flush()  # This clears the session for Trainer
    return redirect('login')




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
    return render(request, 'admin_fn/trainer_home.html')

@login_required
def caretaker_home(request):
    return render(request, 'caretaker_fn/caretaker_home.html')


from django.shortcuts import render, redirect
from .forms import EditProfileForm

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect to a profile page or another relevant page
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

