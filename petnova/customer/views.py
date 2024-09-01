from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from . models import Customer 
from django.contrib import messages


# Create your views here.
def show_account(request):
    if request.POST and 'register' in request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            #create user account .....
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            #create customer account
            customer=Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            success_message="User registered successfully"
            messages.success(request,success_message)
        except Exception as e:
            error_message="invalid inputs"
            messages.error(request,error_message)
    

    if request.POST and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('account')
        else:
            messages.error(request,'invalid user credentials')
            
        




    return render(request,'account.html')
    
