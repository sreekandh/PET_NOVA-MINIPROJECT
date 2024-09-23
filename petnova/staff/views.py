from django.shortcuts import render



# Create your views here.
def staff_info(request):
    return render(request, 'staff/staff_info.html')

def trainer_service(request):
    return render(request, 'staff/trainer_service.html')

def caretaker_service(request):
    return render(request, 'staff/caretaker_service.html')

def about_page(request):
    return render(request,'staff/about_page.html')

def contact_page(request):
    return render(request,'staff/contact_page.html')