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
