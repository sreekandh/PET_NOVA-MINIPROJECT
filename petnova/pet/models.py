# models.py

from django.db import models

class Pet(models.Model):
    CATEGORY_CHOICES = [
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
    ]
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name


from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import os

def validate_image(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only .jpg, .jpeg, and .png are allowed.')

class UserPet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=50, unique=True)
    pet_breed = models.CharField(max_length=50)
    pet_species = models.CharField(max_length=50)
    pet_age = models.PositiveIntegerField(validators=[MinValueValidator(1, message="Age should be at least 1.")])
    pet_image = models.ImageField(upload_to='user_pets/', validators=[validate_image])

    def __str__(self):
        return f'{self.pet_name} ({self.pet_species})'
    
    # Validation for text-only fields
    def clean(self):
        if not self.pet_name.isalpha():
            raise ValidationError('Pet name must contain only letters.')
        if not self.pet_breed.isalpha():
            raise ValidationError('Pet breed must contain only letters.')
        if not self.pet_species.isalpha():
            raise ValidationError('Pet species must contain only letters.')
