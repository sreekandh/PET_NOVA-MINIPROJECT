from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from admin_fn.models import AdoptionApplication



def home(request):
    return render(request,'index.html')
    
def pet_details(request):
    return render(request,'pet/pet_details.html')
    



# views.py

from django.shortcuts import render, get_object_or_404
from .models import Pet

def pet_list(request, category=None):
    if request.user.is_staff:  # Check if the user is an admin
        pets = Pet.objects.all()
    else:
        if category:
            pets = Pet.objects.filter(category=category)
        else:
            pets = Pet.objects.all()
    
    return render(request, 'pet/pet_list.html', {'pets': pets})

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'pet/pet_detail.html', {'pet': pet})

# views.py
from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm

def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pet/pet_form.html', {'form': form})


def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pet/pet_form.html', {'form': form})

def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('pet_list')
    return render(request, 'pet/pet_confirm_delete.html', {'pet': pet})


from django.shortcuts import render, get_object_or_404
from admin_fn.models import Cat, Dog

def cat_list(request):
    cats = Cat.objects.all()
    return render(request, 'pet/cat_list.html', {'cats': cats})

def dog_list(request):
    dogs = Dog.objects.all()
    return render(request, 'pet/dog_list.html', {'dogs': dogs})

def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    return render(request, 'pet/cat_detail.html', {'cat': cat})

def dog_detail(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    return render(request, 'pet/dog_detail.html', {'dog': dog})



from django.shortcuts import render
from admin_fn.models import AdoptionApplication

def app_view(request):
    applications = AdoptionApplication.objects.filter(user=request.user)
    return render(request, 'pet/app_view.html', {'applications': applications})




#############################################################3

#user pet #######################

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import UserPet
from .forms import UserPetForm

# List all user pets
def user_pets_list(request):
    pets = UserPet.objects.filter(user=request.user)
    return render(request, 'pet/user_pets_list.html', {'pets': pets})

# Register a new pet
def register_pet(request):
    if request.method == 'POST':
        form = UserPetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user  # Assign the pet to the logged-in user
            pet.save()
            messages.success(request, "Pet registered successfully.")
            return redirect('user_pets_list')
    else:
        form = UserPetForm()
    return render(request, 'pet/register_pet.html', {'form': form})

# Update pet details
def edit_pet(request, pet_id):
    pet = get_object_or_404(UserPet, id=pet_id, user=request.user)
    if request.method == 'POST':
        form = UserPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet updated successfully.")
            return redirect('user_pets_list')
    else:
        form = UserPetForm(instance=pet)
    return render(request, 'pet/edit_pet.html', {'form': form})

# Delete a pet
def delete_pet(request, pet_id):
    pet = get_object_or_404(UserPet, id=pet_id, user=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet deleted successfully.")
        return redirect('user_pets_list')
    return render(request, 'pet/delete_pet.html', {'pet': pet})
