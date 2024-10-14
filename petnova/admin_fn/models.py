
from django.utils import timezone  # Correctly import Django's timezone
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_caretaker = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'





from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import re

def validate_text(value):
    if not re.match("^[A-Za-z\s]*$", value):  # Only letters and spaces allowed
        raise ValidationError('This field should only contain letters and spaces.')

class Cat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(0)])  # Age cannot be below 0
    breed = models.CharField(max_length=100, validators=[validate_text])  # Only text allowed
    description = models.TextField()
    image = models.ImageField(upload_to='cat_images/')  # Only image uploads
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Price cannot be negative

    def __str__(self):
        return self.name







from django.core.exceptions import ValidationError
from django.db import models

class Dog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='dog_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price field

    def __str__(self):
        return self.name

    def clean(self):
        # Validate age
        if self.age < 0:
            raise ValidationError('Age cannot be negative.')
        
        # Validate price
        if self.price < 0:
            raise ValidationError('Price cannot be negative.')

        # Validate name and breed
        if not self.name.isalpha():
            raise ValidationError('Name should contain only letters.')
        if not self.breed.isalpha():
            raise ValidationError('Breed should contain only letters.')

        # Validate image file type
        if not self.image.name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValidationError('Only image files are allowed (PNG, JPG, JPEG, GIF).')







from django.db import models
from django.conf import settings

class AdoptionApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey('Cat' or 'Dog', on_delete=models.CASCADE)  # Depending on which pet type
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    status = models.CharField(
    max_length=11,  # Updated to fit 'Disapproved'
    choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')],
    default='Pending')
    application_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.full_name} applied for {self.pet.name}'



from django.db import models

class Trainer(models.Model):
    SERVICE_DOG_TRAINING = 'Service dog training'
    AGILITY_TRAINING = 'Agility training'
    K9_TRAINING = 'K-9 training'
    THERAPY_TRAINING = 'Therapy training'
    OBEDIENCE_TRAINING = 'Obedience training'
    NORMAL_PET_TRAINING = 'Normal pet training'

    SPECIALIZATION_CHOICES = [
        (SERVICE_DOG_TRAINING, 'Service dog training'),
        (AGILITY_TRAINING, 'Agility training'),
        (K9_TRAINING, 'K-9 training'),
        (THERAPY_TRAINING, 'Therapy training'),
        (OBEDIENCE_TRAINING, 'Obedience training'),
        (NORMAL_PET_TRAINING, 'Normal pet training'),
    ]

    trainer_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.TextField()  # Description of experience or certifications
    specialization = models.CharField(max_length=255, choices=SPECIALIZATION_CHOICES)  # Dropdown for specialization
    image = models.ImageField(upload_to='trainer_images/')  # Upload path for trainer images
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128, default='defaultpassword')  # Set a default value here

    def __str__(self):
        return self.trainer_name


from django.db import models
class TrainingSlot(models.Model):
    DURATION_CHOICES = [
        (15, '15 Days'),
        (30, '30 Days'),
        (45, '45 Days'),
        (60, '60 Days'),
    ]

    duration = models.IntegerField(choices=DURATION_CHOICES, default=15)  # Default duration in days
    price = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)  # Default price
    methods = models.TextField(default='In-Person')  # Default value for methods
    image = models.ImageField(upload_to='training_slots/', blank=True, null=True)  # Add image field
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='training_slots')  # Add this line

    def __str__(self):
        return f'{self.get_duration_display()} - {self.price} Rs'

from django.db import models

from django.db import models
from django.db import models

class Caretaker(models.Model):
    PET_SITTING = 'Pet Sitting'
    PET_GROOMING = 'Pet Grooming'
    DOG_WALKER = 'Dog Walker'
    PET_FEEDER = 'Pet Feeder'

    SPECIALIZATION_CHOICES = [
        (PET_SITTING, 'Pet Sitting'),
        (PET_GROOMING, 'Pet Grooming'),
        (DOG_WALKER, 'Dog Walker'),
        (PET_FEEDER, 'Pet Feeder'),
    ]

    caretaker_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.TextField()
    specialization = models.CharField(max_length=255, choices=SPECIALIZATION_CHOICES)
    image = models.ImageField(upload_to='caretaker_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128, default='defaultpassword')

    def __str__(self):
        return self.caretaker_name


class CaretakerSlot(models.Model):
    DURATION_CHOICES = [
        (1, '1 Day'),
        (3, '3 Days'),
        (5, '5 Days'),
        (7, '7 Days'),
    ]

    # Allow caretaker field to be null
    caretaker = models.ForeignKey(Caretaker, on_delete=models.SET_NULL, related_name='caretaker_slots', null=True)
    service = models.CharField(max_length=100, choices=Caretaker.SPECIALIZATION_CHOICES)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=1)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)  # Additional cost per day
    image = models.ImageField(upload_to='caretaker_slots/', blank=True, null=True)

    def calculate_total_price(self):
        # Calculate total price based on base price and duration
        return self.base_price + (self.price_per_day * (self.duration - 1))

    def __str__(self):
        return f'{self.service} - {self.get_duration_display()}'



class PetTraining(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the user who booked the training
    owner_name = models.CharField(max_length=100)  # Name of the pet owner
    owner_email = models.EmailField()  # Email of the pet owner
    owner_phone = models.CharField(max_length=15)  # Phone number of the pet owner
    pet_name = models.CharField(max_length=100)  # Name of the pet
    age = models.IntegerField()  # Age of the pet
    image = models.ImageField(upload_to='pet_images/')  # Upload path for pet images
    description = models.TextField()  # Description of the pet
    breed = models.CharField(max_length=100)  # Breed of the pet
    species = models.CharField(max_length=100)  # Species of the pet (e.g., Dog, Cat, etc.)
    training_slot = models.ForeignKey('TrainingSlot', on_delete=models.CASCADE)  # Link to the TrainingSlot
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)  # Link to the Trainer
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the booking was created

    def __str__(self):
        return f'{self.pet_name} - {self.training_slot}'





# Model to represent booking by a user
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Caretaker

User = get_user_model()

class CaretakerSlotBooking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caretaker_bookings')
    service = models.CharField(max_length=255)  # Store as a comma-separated string
    duration = models.PositiveIntegerField(help_text="Duration in days")
    additional_notes = models.TextField(blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # New fields for pet details
    pet_name = models.CharField(max_length=100)
    pet_breed = models.CharField(max_length=100)
    pet_species = models.CharField(max_length=100)
    pet_age = models.PositiveIntegerField()
    pet_image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    service_start_date = models.DateTimeField(default=timezone.now)  # Set default to current time
    
    # New field to track booking status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f'{self.user} booked {self.caretaker} for {self.service}'
