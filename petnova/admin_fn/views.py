import re
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



##################################################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cat
from .forms import CatForm

# Add a new cat
@login_required
def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cat added successfully!')
            return redirect('view_cats')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CatForm()
    
    return render(request, 'admin_fn/add_cat.html', {'form': form})

# View all cats
@login_required
def view_cats(request):
    cats = Cat.objects.all()
    return render(request, 'admin_fn/view_cats.html', {'cats': cats})

# Edit an existing cat
@login_required
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cat details updated successfully!')
            return redirect('view_cats')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CatForm(instance=cat)
    
    return render(request, 'admin_fn/edit_cat.html', {'form': form, 'cat': cat})

# Delete a cat
@login_required
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Cat deleted successfully!')
        return redirect('view_cats')
    
    return render(request, 'admin_fn/delete_cat.html', {'cat': cat})

###############################################



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dog
from .forms import DogForm

# Add a new dog
@login_required
def add_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the dog object to the database
            messages.success(request, 'Dog added successfully!')
            return redirect('view_dogs')  # Redirect to the view displaying all dogs
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DogForm()
    
    return render(request, 'admin_fn/add_dog.html', {'form': form})

# View all dogs
@login_required
def view_dogs(request):
    dogs = Dog.objects.all()
    return render(request, 'admin_fn/view_dogs.html', {'dogs': dogs})

# Edit an existing dog
@login_required
def edit_dog(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()  # Save the updates to the dog object
            messages.success(request, 'Dog details updated successfully!')
            return redirect('view_dogs')  # Redirect after updating
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DogForm(instance=dog)
    
    return render(request, 'admin_fn/edit_dog.html', {'form': form, 'dog': dog})

# Delete a dog
@login_required
def delete_dog(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    
    if request.method == 'POST':
        dog.delete()
        messages.success(request, 'Dog deleted successfully!')
        return redirect('view_dogs')  # Redirect after deletion
    
    return render(request, 'admin_fn/delete_dog.html', {'dog': dog})



#########################################################
# views.py
from django.contrib.auth.models import User

@login_required
def view_registered_users(request):
    users = User.objects.all()
    return render(request, 'admin_fn/view_registered_users.html', {'users': users})


##############################################



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
    
    # Check if the user has already submitted an application
    if request.session.get('adoption_application_submitted', False):
        return redirect('adoption_success')
    
    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.pet = pet
            application.save()
            
            # Set session variable to indicate the application has been submitted
            request.session['adoption_application_submitted'] = True
            
            # Redirect to a success page
            return redirect('adoption_success')
    else:
        # Pre-fill the form with logged-in user's data
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'email': user.email,
        }
        form = AdoptionApplicationForm(initial=initial_data)
    
    return render(request, 'pet/adopt_form.html', {'form': form, 'pet': pet}) 


from django.shortcuts import render

def adoption_success(request):
    # Optionally, you can clear the session variable here or when the user logs out
    # request.session.pop('adoption_application_submitted', None)
    return render(request, 'pet/adoption_success.html') 

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


#####################################################################

def user_home(request):
    applications = AdoptionApplication.objects.filter(user=request.user)
    return render(request, 'index.html', {'applications': applications})




########################################################
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
############################################################


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

################################################################

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


############################################################

def cat(request):
    return render(request,'admin_fn/cat.html')



def dog(request):
    return render(request,'admin_fn/dog.html')


###########################################################
'''
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

'''

###############################################


from django.shortcuts import render, redirect
from .forms import TrainerForm

def register_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            # Directly assign the password without hashing it
            trainer.password = form.cleaned_data['password']
            trainer.save()
            return redirect('view_trainers')  # Redirect to a page that lists trainers or similar
    else:
        form = TrainerForm()
    
    return render(request, 'admin_fn/register_trainer.html', {'form': form})

# View to display all registered trainers
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trainer

def view_trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'admin_fn/view_trainers.html', {'trainers': trainers})

def activate_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.is_active = True
    trainer.save()
    return redirect('view_trainers')

def deactivate_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.is_active = False
    trainer.save()
    return redirect('view_trainers')


from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings

def send_email_to_trainer(trainer):
    subject = "Your Trainer Account Details"
    message = f"Hello {trainer.trainer_name},\n\nYour username is: {trainer.email}\nYour password is: {trainer.password}\n\nBest Regards,\nPet Nova Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [trainer.email]
    
    send_mail(subject, message, from_email, recipient_list)



from django.contrib.auth.hashers import make_password

def send_trainer_email(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        # Make sure to hash the password if you're storing it as plain text
        trainer.password = make_password(trainer.password)  # Securely hash the password
        trainer.save()  # Save the hashed password
        send_email_to_trainer(trainer)
        return redirect('view_trainers')  # Redirect back to the trainers list
    except Trainer.DoesNotExist:
        return redirect('view_trainers')  # Handle trainer not found

######################################################################

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CaretakerForm
from .models import Caretaker
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

# View to register a caretaker
from django.shortcuts import render, redirect
from .forms import CaretakerForm

def register_caretaker(request):
    if request.method == 'POST':
        form = CaretakerForm(request.POST, request.FILES)
        if form.is_valid():
            caretaker = form.save(commit=False)
            # Directly assign the password without hashing it
            caretaker.password = form.cleaned_data['password']
            caretaker.save()
            return redirect('view_caretakers')  # Redirect to a page that lists caretakers or similar
    else:
        form = CaretakerForm()
    
    return render(request, 'admin_fn/register_caretaker.html', {'form': form})

# View to display all registered caretakers
from django.shortcuts import render
from .models import Caretaker

def view_caretakers(request):
    caretakers = Caretaker.objects.all()
    return render(request, 'admin_fn/view_caretakers.html', {'caretakers': caretakers})

# View to activate a caretaker
def activate_caretaker(request, id):
    caretaker = get_object_or_404(Caretaker, id=id)
    caretaker.is_active = True
    caretaker.save()
    return redirect('view_caretakers')

# View to deactivate a caretaker
def deactivate_caretaker(request, id):
    caretaker = get_object_or_404(Caretaker, id=id)
    caretaker.is_active = False
    caretaker.save()
    return redirect('view_caretakers')

# Function to send email to caretaker
from django.core.mail import send_mail
from django.conf import settings

def send_email_to_caretaker(caretaker):
    subject = "Your Caretaker Account Details"
    message = f"Hello {caretaker.caretaker_name},\n\nYour username is: {caretaker.email}\nYour password is: {caretaker.password}\n\nBest Regards,\nPet Nova Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [caretaker.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")  # Log the error
  # Log the error

# View to send email to caretaker
from django.shortcuts import render, redirect, get_object_or_404
from .models import Caretaker
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

def send_caretaker_email(request, caretaker_id):
    try:
        caretaker = get_object_or_404(Caretaker, id=caretaker_id)
        # Make sure to hash the password if you're storing it as plain text
        caretaker.password = make_password(caretaker.password)  # Securely hash the password
        caretaker.save()  # Save the hashed password
        send_email_to_caretaker(caretaker)
        return redirect('view_caretakers')  # Redirect back to the caretakers list
    except Caretaker.DoesNotExist:
        return redirect('view_caretakers')  # Handle caretaker not found

######################################################################


def trainer_profile(request):
    # Your profile page view logic
    return render(request, 'admin_fn/trainer_profile.html')

###############################################################

from django.shortcuts import render
from django.http import HttpResponse
from datetime import timedelta

def schedule_training_section(request):
    if request.method == 'POST':
        # Get the selected training duration and start date
        duration = int(request.POST.get('training_duration'))
        start_date = request.POST.get('start_date')

        # Calculate the price based on the selected duration
        price = 3000 + ((duration // 15 - 1) * 2000)

        # For now, let's just return a confirmation message
        return HttpResponse(f"Training slot booked for {duration} days starting on {start_date}. Total cost: {price} Rs.")
    
    return render(request, 'admin_fn/schedule_training_section.html')

from django.shortcuts import render, get_object_or_404
from .models import Trainer, TrainingSlot  # Assuming you have a TrainingSlot model

def view_training_slots(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    training_slots = TrainingSlot.objects.filter(trainer=trainer, is_booked=False)  # Assuming is_booked marks booked slots
    context = {
        'trainer': trainer,
        'training_slots': training_slots,
    }
    return render(request, 'admin_fn/view_training_slots.html', context)




from django.shortcuts import redirect, get_object_or_404
from .models import TrainingSlot

def book_training_slot(request, slot_id):
    slot = get_object_or_404(TrainingSlot, id=slot_id)

    # Mark the slot as booked
    slot.is_booked = True
    slot.save()

    return redirect('view_training_slots', trainer_id=slot.trainer.id)

from django.shortcuts import render, get_object_or_404
from .models import Trainer, TrainingSlot

#######################################################

# View for displaying the list of registered trainers
def user_view_trainers(request):
    trainers = Trainer.objects.filter(is_active=True)  # Assuming you only want to show active trainers
    context = {
        'trainers': trainers,
    }
    return render(request, 'admin_fn/user_view_trainers.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingSlot
from .forms import TrainingSlotForm

# List all training slots
def list_training_slots(request):
    slots = TrainingSlot.objects.all()
    return render(request, 'admin_fn/list_training_slots.html', {'slots': slots})

# Add new training slot
from django.shortcuts import render, redirect
from .models import TrainingSlot
from .forms import TrainingSlotForm

def add_training_slot(request):
    if request.method == 'POST':
        form = TrainingSlotForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('list_training_slots')  # Redirect after successful save
    else:
        form = TrainingSlotForm()
    
    return render(request, 'admin_fn/add_training_slot.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import TrainingSlot
from .forms import TrainingSlotForm

def edit_training_slot(request, slot_id):  # Accept slot_id as parameter
    slot = get_object_or_404(TrainingSlot, pk=slot_id)

    if request.method == 'POST':
        form = TrainingSlotForm(request.POST, request.FILES, instance=slot)
        if form.is_valid():
            form.save()
            return redirect('list_training_slots')  # Redirect after saving
    else:
        form = TrainingSlotForm(instance=slot)

    return render(request, 'admin_fn/edit_training_slot.html', {'form': form})

# Delete an existing training slot
def delete_training_slot(request, slot_id):
    slot = get_object_or_404(TrainingSlot, id=slot_id)
    if request.method == 'POST':
        slot.delete()
        return redirect('list_training_slots')
    
    return render(request, 'admin_fn/delete_training_slot.html', {'slot': slot})

###################################################


from django.shortcuts import render
from .models import TrainingSlot

def user_list_training_slots(request):
    slots = TrainingSlot.objects.all()  # Fetch all training slots
    return render(request, 'admin_fn/user_list_training_slots.html', {'slots': slots})





from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import TrainingSlot, Trainer, PetTraining  # Make sure PetTraining is defined in your models
from django.core.mail import send_mail
from django.conf import settings



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TrainingSlot, PetTraining

def trainer_slot_booking_view(request, slot_id):
    # Fetch the selected slot and the corresponding trainer
    slot = get_object_or_404(TrainingSlot, id=slot_id)
    trainer = slot.trainer  # Now we can access the trainer directly

    if request.method == 'POST':
        # Get form data
        owner_name = request.POST.get('owner_name')
        owner_email = request.POST.get('owner_email')
        owner_phone = request.POST.get('owner_phone')
        pet_name = request.POST.get('pet_name')
        age = request.POST.get('age')
        image = request.FILES.get('image')  # Handle the uploaded file
        description = request.POST.get('description')
        breed = request.POST.get('breed')
        species = request.POST.get('species')

        # Perform basic validation
        if not all([owner_name, owner_email, owner_phone, pet_name, age, description, breed, species]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'admin_fn/slot_book.html', {
                'slot': slot,
                'trainer': trainer
            })

        # Save the booking details to the PetTraining model
        pet_training = PetTraining.objects.create(
            user=request.user,  # Link the user who booked the training
            pet_name=pet_name,
            age=age,
            image=image,
            description=description,
            breed=breed,
            species=species,
            training_slot=slot,  # Link the training slot to the booking
            trainer=trainer,  # Assuming you have a field for trainer in your PetTraining model
            owner_name=owner_name,  # New field
            owner_email=owner_email,  # New field
            owner_phone=owner_phone,  # New field
        )

        # Send email notification to admin
        send_mail(
            subject='New Training Slot Booking',
            message=f'A new training slot has been booked for {pet_name} by {owner_name}.\nEmail: {owner_email}\nPhone: {owner_phone}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['sreekandh1212@gmail.com'],  # Admin email
        )

        # Send email notification to trainer
        send_mail(
            subject='New Training Slot Booking',
            message=f'You have a new training slot booked for {pet_name} by {owner_name}.\nEmail: {owner_email}\nPhone: {owner_phone}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[trainer.email],  # Trainer's email
        )

        messages.success(request, 'Booking confirmed! You will be notified shortly.')
        return redirect('user_list_training_slots')  # Redirect to a success page after booking

    return render(request, 'admin_fn/slot_book.html', {
        'slot': slot,
        'trainer': trainer
    })




########################################################

# views.py
from django.shortcuts import render
from .models import PetTraining  # Adjust the import based on your structure

def admin_view_bookings(request):
    bookings = PetTraining.objects.select_related('training_slot', 'trainer').all()
    return render(request, 'admin_fn/admin_view_bookings.html', {'bookings': bookings})


from django.shortcuts import render, redirect
from .forms import CaretakerSlotForm
from .models import CaretakerSlot

from django.shortcuts import render, redirect
from .forms import CaretakerSlotForm

from django.shortcuts import render, redirect
from .forms import CaretakerSlotForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CaretakerSlotForm

from django.shortcuts import render, redirect
from .forms import CaretakerSlotForm

##############################################################3

def assign_caretaker_slot(request):
    if request.method == 'POST':
        form = CaretakerSlotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # This will now work without raising IntegrityError
            return redirect('list_caretaker_slots')
    else:
        form = CaretakerSlotForm()

    return render(request, 'admin_fn/assign_caretaker_slot.html', {'form': form})

from django.shortcuts import render
from .models import CaretakerSlot

from django.shortcuts import render
from .models import CaretakerSlot

def list_caretaker_slots(request):
    slots = CaretakerSlot.objects.all()  # Fetch all caretaker slots
    return render(request, 'admin_fn/list_caretaker_slots.html', {'slots': slots})


from django.shortcuts import render, redirect


from django.shortcuts import get_object_or_404

def edit_caretaker_slot(request, slot_id):
    slot = get_object_or_404(CaretakerSlot, pk=slot_id)  # Get the slot or return a 404

    if request.method == 'POST':
        form = CaretakerSlotForm(request.POST, request.FILES, instance=slot)  # Bind the form to the slot
        if form.is_valid():
            form.save()  # Save changes
            return redirect('list_caretaker_slots')  # Redirect after saving
    else:
        form = CaretakerSlotForm(instance=slot)  # Populate the form with existing slot data

    return render(request, 'admin_fn/edit_caretaker_slot.html', {'form': form})


def delete_caretaker_slot(request, slot_id):
    slot = get_object_or_404(CaretakerSlot, id=slot_id)  # Get the slot or return a 404

    if request.method == 'POST':
        slot.delete()  # Delete the slot
        return redirect('list_caretaker_slots')  # Redirect after deletion
    
    return render(request, 'admin_fn/delete_caretaker_slot.html', {'slot': slot})

#######################################################################



from django.shortcuts import render, get_object_or_404, redirect
from .models import Caretaker, CaretakerSlot

# View to list all available caretakers for users
def user_view_caretaker(request):
    caretakers = Caretaker.objects.filter(is_active=True)  # Show only active caretakers
    return render(request, 'admin_fn/user_view_caretaker.html', {'caretakers': caretakers})



##################################################################3

from django.shortcuts import render, get_object_or_404, redirect
from .models import Caretaker, CaretakerSlot
from .forms import CaretakerSlotBookingForm  # Assuming you have a form for booking
from django.shortcuts import render, get_object_or_404, redirect
from .models import Caretaker, CaretakerSlotBooking
from .forms import CaretakerSlotBookingForm
from .models import Caretaker, CaretakerSlotBooking  # Assuming a Pet model exists
from pet.models import UserPet

@login_required
def book_caretaker_slot(request, caretaker_id):
    caretaker = get_object_or_404(Caretaker, id=caretaker_id)
    
    # Fetch the user's first pet (as an example; handle multiple pets as needed)
    pet = UserPet.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = CaretakerSlotBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.caretaker = caretaker
            booking.user = request.user
            booking.service = ', '.join(form.cleaned_data['service'])
            booking.total_price = form.calculate_price()
            booking.save()
            
            # Redirect to payment page with booking id and total price
            return redirect('payment_page', booking_id=booking.id)
    else:
        # Pre-fill the form with pet information if available
        if pet:
            form = CaretakerSlotBookingForm(initial={
                'pet_name': pet.pet_name,
                'pet_breed': pet.pet_breed,
                'pet_species': pet.pet_species,
                'pet_age': pet.pet_age,
                'pet_image': pet.pet_image,
            })
        else:
            form = CaretakerSlotBookingForm()

    return render(request, 'admin_fn/booking_form.html', {'caretaker': caretaker, 'form': form})



def booking_success(request):
    return render(request, 'admin_fn/booking_success.html')



from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CaretakerSlotBooking

def admin_user_caretaker_view(request):
    # Fetch all bookings with related caretaker and user, ordered by booking date (most recent first)
    bookings = CaretakerSlotBooking.objects.select_related('caretaker', 'user').order_by('-booking_date')

    # Pagination
    paginator = Paginator(bookings, 10)  # Show 10 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_fn/admin_user_caretaker_view.html', {'page_obj': page_obj})


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import TrainerSlotBooking  # Adjust the import based on your models

def admin_user_trainer_view(request):
    # Fetch all bookings with related trainer and user, ordered by booking date (most recent first)
    bookings = TrainerSlotBooking.objects.select_related('trainer', 'user').order_by('-booking_date')

    # Pagination
    paginator = Paginator(bookings, 10)  # Show 10 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_fn/admin_user_trainer_view.html', {'page_obj': page_obj})


from django.shortcuts import render
from .models import CaretakerSlotBooking
from django.contrib.auth.decorators import login_required


def user_caretaker_bookings(request):
    # Get the bookings for the current user
    bookings = CaretakerSlotBooking.objects.filter(user=request.user)

    context = {
        'bookings': bookings,
    }
    return render(request, 'admin_fn/user_view_caretaker_bookings.html', context)




############################################3

import re
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import CaretakerSlotBooking, Caretaker
from datetime import datetime

def payment_page(request, booking_id):
    booking = get_object_or_404(CaretakerSlotBooking, id=booking_id)
    caretaker = booking.caretaker  # Get the caretaker details

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Validate card number (16 digits)
        if not card_number or len(card_number) != 16 or not card_number.isdigit():
            return render(request, 'admin_fn/payment_page.html', {'booking': booking, 'error': 'Invalid card number'})

        # Validate expiry date (MM/YY format)
        if not expiry_date or not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', expiry_date):
            return render(request, 'admin_fn/payment_page.html', {'booking': booking, 'error': 'Invalid expiry date format'})

        # Check if the expiry date is in the past
        month, year = map(int, expiry_date.split('/'))
        current_month = datetime.now().month
        current_year = datetime.now().year % 100  # Get last two digits of the year

        if year < current_year or (year == current_year and month < current_month):
            return render(request, 'admin_fn/payment_page.html', {'booking': booking, 'error': 'Expiry date cannot be in the past.'})

        # Validate CVV (3 digits)
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            return render(request, 'admin_fn/payment_page.html', {'booking': booking, 'error': 'Invalid CVV'})

        # If payment is successful, send email to both the admin and the caretaker (trainer)
        send_booking_email(booking)

        # Assuming payment is successful
        return redirect('payment_success')

    return render(request, 'admin_fn/payment_page.html', {'booking': booking})



# Helper function to send email notifications
# Helper function to send email notifications
def send_booking_email(booking):
    subject = f'New Caretaker Slot Booking for {booking.caretaker.caretaker_name}'  # Change here
    message = (
        f'A new booking has been made by {booking.user.first_name} {booking.user.last_name}.\n\n'
        f'Booking Details:\n'
        f'Service: {booking.service}\n'
        f'Duration: {booking.duration} days\n'
        f'Additional Notes: {booking.additional_notes}\n'
        f'Total Price: {booking.total_price} USD\n\n'
        f'Pet Details:\n'
        f'Name: {booking.pet_name}\n'
        f'Breed: {booking.pet_breed}\n'
        f'Species: {booking.pet_species}\n'
        f'Age: {booking.pet_age}\n\n'
        f'Please review the booking in your system.'
    )

    # Send email to the admin
    admin_email = settings.ADMIN_EMAIL  # Make sure this is defined in your settings
    trainer_email = booking.caretaker.email  # Assuming caretaker has an email field

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email, trainer_email],  # Send to both admin and caretaker (trainer)
        fail_silently=False,
    )


def payment_success(request):
    return render(request, 'admin_fn/payment_success.html')


def booking_cancel(request, booking_id):
    # Handle booking cancellation logic
    return redirect('home') 


from django.shortcuts import render, redirect, get_object_or_404
from .models import CaretakerSlotBooking  # Adjust this import based on your models
@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(CaretakerSlotBooking, id=booking_id)
        booking.status = 'canceled'  # Update the booking status to canceled
        booking.save()  # Save the changes
        # Optionally, add a success message here
        return redirect('user_caretaker_bookings')  # Redirect to bookings page

    return redirect('user_caretaker_bookings')  # Redirect if not a POST request


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainerSlotBooking  # Adjust this import based on your models

def user_trainer_bookings(request):
    # Get the bookings for the current user
    bookings = TrainerSlotBooking.objects.filter(user=request.user)

    context = {
        'bookings': bookings,
    }
    return render(request, 'admin_fn/user_view_trainer_bookings.html', context)

def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(TrainerSlotBooking, id=booking_id)
        booking.status = 'canceled'  # Update the booking status to canceled
        booking.save()  # Save the changes
        return redirect('user_trainer_bookings')  # Redirect to bookings page

    return redirect('user_trainer_bookings')  # Redirect if not a POST request


################################################



from django.shortcuts import render, get_object_or_404, redirect
from .models import Trainer, TrainerSlotBooking
from .forms import TrainerSlotBookingForm

@login_required
def book_trainer_slot(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    pet = UserPet.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = TrainerSlotBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trainer = trainer
            booking.user = request.user
            booking.service = ', '.join(form.cleaned_data['service'])
            booking.total_price = form.calculate_price()
            booking.save()
            request.session['booking_made'] = True  # Set session variable
            return redirect('trainer_payment_page', booking_id=booking.id)
    else:
        if pet:
            form = TrainerSlotBookingForm(initial={
                'pet_name': pet.pet_name,
                'pet_breed': pet.pet_breed,
                'pet_species': pet.pet_species,
                'pet_age': pet.pet_age,
                'pet_image': pet.pet_image,
            })
        else:
            form = TrainerSlotBookingForm()

    return render(request, 'admin_fn/trainer_booking_form.html', {'trainer': trainer, 'form': form})


import re
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import TrainerSlotBooking, Trainer
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required

def trainer_payment_page(request, booking_id):
    booking = get_object_or_404(TrainerSlotBooking, id=booking_id)  # Change to TrainerSlotBooking
    trainer = booking.trainer  # Get the trainer details

    if not request.session.get('booking_made', False):
        return redirect('book_trainer_slot') 

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Validate card number (16 digits)
        if not card_number or len(card_number) != 16 or not card_number.isdigit():
            return render(request, 'admin_fn/trainer_payment_page.html', {'booking': booking, 'error': 'Invalid card number'})

        # Validate expiry date (MM/YY format)
        if not expiry_date or not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', expiry_date):
            return render(request, 'admin_fn/trainer_payment_page.html', {'booking': booking, 'error': 'Invalid expiry date format'})

        # Check if the expiry date is in the past
        month, year = map(int, expiry_date.split('/'))
        current_month = datetime.now().month
        current_year = datetime.now().year % 100  # Get last two digits of the year

        if year < current_year or (year == current_year and month < current_month):
            return render(request, 'admin_fn/trainer_payment_page.html', {'booking': booking, 'error': 'Expiry date cannot be in the past.'})

        # Validate CVV (3 digits)
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            return render(request, 'admin_fn/trainer_payment_page.html', {'booking': booking, 'error': 'Invalid CVV'})

        # Assuming payment is successful
        send_trainer_booking_email(booking)
        del request.session['booking_made'] 

        return redirect('payment_success')

    return render(request, 'admin_fn/trainer_payment_page.html', {'booking': booking})

def send_trainer_booking_email(booking):
    subject = f'New Trainer Slot Booking for {booking.trainer.trainer_name}'
    message = (
        f'A new booking has been made by {booking.user.first_name} {booking.user.last_name}.\n\n'
        f'Booking Details:\n'
        f'Service: {booking.service}\n'
        f'Duration: {booking.duration} days\n'
        f'Additional Notes: {booking.additional_notes}\n'
        f'Total Price: {booking.total_price} USD\n\n'
        f'Pet Details:\n'
        f'Name: {booking.pet_name}\n'
        f'Breed: {booking.pet_breed}\n'
        f'Species: {booking.pet_species}\n'
        f'Age: {booking.pet_age}\n\n'
        f'Please review the booking in your system.'
    )

    admin_email = settings.ADMIN_EMAIL  # Ensure this is set in your settings
    trainer_email = booking.trainer.email  # Assuming Trainer model has an email field

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email, trainer_email],
        fail_silently=False,
    )

def payment_success(request):
    return render(request, 'admin_fn/payment_success.html')


def admin_dashboard(request):
    return render(request ,'admin_fn/admin_dashboard.html')


def view_cat_trainer(request):
    return render(request,'admin_fn/view_cat_trainer.html')

def view_dog_trainer(request):
    return render(request,'admin_fn/view_dog_trainer.html')


def view_cat_caretaker(request):
    return render(request,'admin_fn/view_cat_caretaker.html')

def view_dog_caretaker(request):
    return render(request,'admin_fn/view_dog_caretaker.html')

