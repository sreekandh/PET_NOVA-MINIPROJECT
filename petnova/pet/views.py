from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request,'index.html')
    
def pet_details(request):
    return render(request,'pet/pet_details.html')
    
def cat_details(request):
    return render(request,'pet/cat_details.html')

def dog_details(request):
    return render(request,'pet/dog_details.html')