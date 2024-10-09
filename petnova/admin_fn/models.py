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

# models.py
from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='cat_images/')  # Add this line

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='dog_images/')  # Add this line

    def __str__(self):
        return self.name


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
    trainer_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.TextField()  # Description of experience or certifications
    specialization = models.CharField(max_length=255)  # Field for trainer specialization
    image = models.ImageField(upload_to='trainer_images/')  # Upload path for trainer images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trainer_name

 
from django.db import models

class Caretaker(models.Model):
    caretaker_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.TextField()  # Description of experience or certifications
    specialization = models.CharField(max_length=255)  # Field for caretaker specialization
    image = models.ImageField(upload_to='caretaker_images/')  # Upload path for caretaker images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caretaker_name
