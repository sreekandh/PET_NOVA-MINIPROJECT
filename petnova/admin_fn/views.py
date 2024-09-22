from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


    
def admin_function(request):
    return render(request,'admin_fn/admin_function.html')
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            
            # Check role and redirect accordingly
            if user.is_admin:
                return redirect('admin_home')
            elif user.is_trainer:
                return redirect('trainer_home')
            elif user.is_caretaker:
                return redirect('caretaker_home')
        else:
            # Invalid login
            return render(request, 'admin_fn/admin_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'admin_fn/admin_login.html')


def trainer_home(request):
    return render(request,'admin_fn/trainer_home.html')

def caretaker_home(request):
    return render(request,'admin_fn/caretaker_home.html')

def admin_home(request):
    return render(request,'admin_fn/admin_home.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')

# views.py

from django.contrib.auth import get_user_model
from django.shortcuts import render

def admin_users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'admin_fn/admin_user.html', {'users': users})
