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
    pending_applications = AdoptionApplication.objects.filter(status='Pending')
    return render(request, 'admin_fn/admin_home.html', {'pending_applications': pending_applications})


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


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cat
from .forms import CatForm

@login_required
def view_cats(request):
    cats = Cat.objects.all()
    return render(request, 'admin_fn/view_cats.html', {'cats': cats})

@login_required
def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_cats')
    else:
        form = CatForm()
    return render(request, 'admin_fn/add_cat.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat
from .forms import CatForm
@login_required
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    if request.method == 'POST':
        form = CatForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('view_cats')  # Adjust the redirect URL to your URL name
    else:
        form = CatForm(instance=cat)

    return render(request, 'admin_fn/edit_cat.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat
@login_required
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    
    if request.method == 'POST':
        cat.delete()
        return redirect('view_cats')  # Redirect after deletion
    
    return render(request, 'admin_fn/delete_cat.html', {'cat': cat})


# views.py
from .models import Dog
from .forms import DogForm

@login_required
def view_dogs(request):
    dogs = Dog.objects.all()
    return render(request, 'admin_fn/view_dogs.html', {'dogs': dogs})

@login_required
def add_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_dogs')
    else:
        form = DogForm()
    return render(request, 'admin_fn/add_dog.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Dog
from .forms import DogForm
@login_required
def edit_dog(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('view_dogs')  # Adjust the redirection as per your need
    else:
        form = DogForm(instance=dog)
    
    return render(request, 'admin_fn/edit_dog.html', {'form': form})





from django.shortcuts import render, get_object_or_404, redirect
from .models import Dog
@login_required
def delete_dog(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    
    if request.method == 'POST':
        dog.delete()
        return redirect('view_dogs')  # Adjust the redirect as necessary
    
    return render(request, 'admin_fn/delete_dog.html', {'dog': dog})


# views.py
from django.contrib.auth.models import User

@login_required
def view_registered_users(request):
    users = User.objects.all()
    return render(request, 'admin_fn/view_registered_users.html', {'users': users})

from django.shortcuts import render
from .forms import CatForm

def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_cat')
    else:
        form = CatForm()
    return render(request, 'admin_fn/add_cat.html', {'form': form})  # Ensure this path is correct

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dog  # Assuming you have a Dog model
from .forms import DogForm  # Assuming you have a DogForm for your form

def add_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the dog object to the database
            messages.success(request, 'Dog added successfully!')
            return redirect('view_dogs')  # Redirect to a view displaying all dogs or elsewhere
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = DogForm()
    
    return render(request, 'admin_fn/add_dog.html', {'form': form})


def approve_application(request, application_id):
    application = get_object_or_404(AdoptionApplication, id=application_id)
    application.status = 'Approved'
    application.save()
    return redirect('admin_home')

def disapprove_application(request, application_id):
    application = get_object_or_404(AdoptionApplication, id=application_id)
    application.status = 'Disapproved'
    application.save()
    return redirect('admin_home')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat, Dog, AdoptionApplication
from .forms import AdoptionApplicationForm

def apply_for_adoption(request, pet_id, pet_type):
    pet_model = Cat if pet_type == 'cat' else Dog
    pet = get_object_or_404(pet_model, id=pet_id)
    
    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.pet = pet
            application.save()
            # Redirect to a success page or message
            return redirect('adoption_success')
    else:
        form = AdoptionApplicationForm()
    
    return render(request, 'pet/adopt_form.html', {'form': form, 'pet': pet})


from django.shortcuts import render

def adoption_success(request):
    return render(request, 'pet/adoption_success.html')  # Create this template

from django.shortcuts import render
from .models import AdoptionApplication

def view_applications(request):
    # Order applications by 'application_date' in descending order (latest first)
    applications = AdoptionApplication.objects.all().order_by('-application_date')
    
    return render(request, 'admin_fn/applications.html', {'applications': applications})





from django.core.mail import send_mail
from django.conf import settings

def approve_application(request, application_id):
    application = get_object_or_404(AdoptionApplication, id=application_id)
    application.status = 'approved'
    application.save()

    # Send email notification
    send_mail(
        'Adoption Application Approved',
        f'Your application for {application.pet.name} has been approved. Message from admin: {application.feedback}',
        settings.DEFAULT_FROM_EMAIL,
        [application.user.email],
        fail_silently=False,
    )
    return redirect('admin_home')

def disapprove_application(request, application_id):
    application = get_object_or_404(AdoptionApplication, id=application_id)
    application.status = 'disapproved'
    application.save()

    # Send email notification
    send_mail(
        'Adoption Application Disapproved',
        f'Your application for {application.pet.name} has been disapproved. Message from admin: {application.feedback}',
        settings.DEFAULT_FROM_EMAIL,
        [application.user.email],
        fail_silently=False,
    )
    return redirect('admin_home')




def user_home(request):
    applications = AdoptionApplication.objects.filter(user=request.user)
    return render(request, 'index.html', {'applications': applications})


# In pet/views.py
# admin_fn/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import AdoptionApplication

def make_payment(request, application_id):
    application = get_object_or_404(AdoptionApplication, id=application_id)
    if request.method == "POST":
        # Handle payment processing logic here
        # After successful payment, update payment status
        application.payment_status = True
        application.save()
        return redirect('payment_success')  # Redirect to a success page

    return render(request, 'pet/make_payment.html', {'application': application})

# admin_fn/views.py
from django.shortcuts import render

def payment_success(request):
    return render(request, 'pet/payment_success.html')



from django.shortcuts import render
from .models import AdoptionApplication

def apply_control(request):
    # Fetch pending applications from the database
    pending_applications = AdoptionApplication.objects.filter(status='pending')
    
    # Pass the pending applications to the template
    return render(request, 'admin_fn/apply_control.html', {'pending_applications': pending_applications})


def view_pets(request):
    return render(request,'admin_fn/view_pets.html')


def add_pets(request):
    return render(request,'admin_fn/add_pets.html')

def staff_control(request):
    return render(request,'staff/staff_control.html')

def trainer_con(request):
    return render(request,'staff/trainer_con.html')

def caretaker_con(request):
    return render(request,'staff/caretaker_con.html')



from django.shortcuts import render, redirect, get_object_or_404
from .models import Trainer
from .forms import TrainerForm
from django.contrib import messages

# View all trainers
def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'admin_fn/trainer_list.html', {'trainers': trainers})

# Add a new trainer
def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainer added successfully!")
            return redirect('trainer_list')
    else:
        form = TrainerForm()
    return render(request, 'admin_fn/add_trainer.html', {'form': form})

# Edit an existing trainer
def edit_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainer updated successfully!")
            return redirect('trainer_list')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'admin_fn/edit_trainer.html', {'form': form, 'trainer': trainer})

# Delete a trainer
def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    if request.method == 'POST':
        trainer.delete()
        messages.success(request, "Trainer deleted successfully!")
        return redirect('trainer_list')
    return render(request, 'admin_fn/delete_trainer.html', {'trainer': trainer})


def cat(request):
    return render(request,'admin_fn/cat.html')



def dog(request):
    return render(request,'admin_fn/dog.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Trainer
from .forms import TrainerForm

def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_trainer')  # Redirect to the list of trainers
    else:
        form = TrainerForm()
    return render(request, 'admin_fn/add_trainer.html', {'form': form})

def view_trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'admin_fn/view_trainers.html', {'trainers': trainers})

def edit_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('view_trainers')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'admin_fn/edit_trainer.html', {'form': form, 'trainer': trainer})

def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    if request.method == 'POST':
        trainer.delete()
        return redirect('view_trainers')
    return render(request, 'admin_fn/delete_trainer.html', {'trainer': trainer})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Caretaker
from .forms import CaretakerForm

def add_caretaker(request):
    if request.method == 'POST':
        form = CaretakerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_caretaker')  # Redirect to the list of caretakers
    else:
        form = CaretakerForm()
    return render(request, 'admin_fn/add_caretaker.html', {'form': form})

def view_caretakers(request):
    caretakers = Caretaker.objects.all()
    return render(request, 'admin_fn/view_caretakers.html', {'caretakers': caretakers})

def edit_caretaker(request, caretaker_id):
    caretaker = get_object_or_404(Caretaker, id=caretaker_id)
    if request.method == 'POST':
        form = CaretakerForm(request.POST, request.FILES, instance=caretaker)
        if form.is_valid():
            form.save()
            return redirect('view_caretakers')
    else:
        form = CaretakerForm(instance=caretaker)
    return render(request, 'admin_fn/edit_caretaker.html', {'form': form, 'caretaker': caretaker})

def delete_caretaker(request, caretaker_id):
    caretaker = get_object_or_404(Caretaker, id=caretaker_id)
    if request.method == 'POST':
        caretaker.delete()
        return redirect('view_caretakers')
    return render(request, 'admin_fn/delete_caretaker.html', {'caretaker': caretaker})
