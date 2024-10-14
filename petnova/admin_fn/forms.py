import re
from django import forms
from .models import Cat, Dog




# Form for Cat model
from django import forms
from .models import Cat
import re

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'description', 'image', 'price']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        age = cleaned_data.get("age")
        price = cleaned_data.get("price")
        
        # Validate that name is unique, excluding the current instance if editing
        if self.instance.pk:  # Check if form is updating an existing instance
            if Cat.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                self.add_error('name', 'A cat with this name already exists.')
        else:
            if Cat.objects.filter(name=name).exists():
                self.add_error('name', 'A cat with this name already exists.')

        # Validate that age is non-negative
        if age is not None and age < 0:
            self.add_error('age', 'Age cannot be negative.')

        # Validate that price is non-negative
        if price is not None and price < 0:
            self.add_error('price', 'Price cannot be negative.')

        # Validate that breed contains only letters and spaces
        breed = cleaned_data.get("breed")
        if breed and not re.match(r"^[A-Za-z\s]*$", breed):  # Use raw string here
            self.add_error('breed', 'Breed should only contain letters and spaces.')

        return cleaned_data


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'age', 'breed', 'description', 'image', 'price']  # Include price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        age = cleaned_data.get("age")
        price = cleaned_data.get("price")
        
        # Validate that name is unique, excluding the current instance if editing
        if self.instance.pk:  # Check if form is updating an existing instance
            if Dog.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                self.add_error('name', 'A dog with this name already exists.')
        else:
            if Dog.objects.filter(name=name).exists():
                self.add_error('name', 'A dog with this name already exists.')

        # Validate that age is non-negative
        if age is not None and age < 0:
            self.add_error('age', 'Age cannot be negative.')

        # Validate that price is non-negative
        if price is not None and price < 0:
            self.add_error('price', 'Price cannot be negative.')

        # Validate that name and breed contain only letters
        if name and not name.isalpha():
            self.add_error('name', 'Name should contain only letters.')
        breed = cleaned_data.get("breed")
        if breed and not breed.isalpha():
            self.add_error('breed', 'Breed should contain only letters.')

        return cleaned_data


from django import forms
from .models import AdoptionApplication

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ['full_name', 'phone', 'email', 'address']


#from django import forms
#from .models import Trainer

#class TrainerForm(forms.ModelForm):
 #   class Meta:
 #       model = Trainer
 #       fields = ['trainer_name', 'email', 'phone', 'experience', 'specialization', 'image']



from django import forms
from .models import Trainer

class TrainerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=128)

    class Meta:
        model = Trainer
        fields = ['trainer_name', 'email', 'phone', 'experience', 'specialization', 'image', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Trainer.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number with at least 10 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


from django import forms
from .models import Caretaker

class CaretakerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=128)

    class Meta:
        model = Caretaker
        fields = ['caretaker_name', 'email', 'phone', 'experience', 'specialization', 'image', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Caretaker.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number with at least 10 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


from django import forms
from .models import TrainingSlot

from django import forms
from .models import TrainingSlot

from django import forms
from .models import TrainingSlot

class TrainingSlotForm(forms.ModelForm):
    class Meta:
        model = TrainingSlot
        fields = ['duration', 'price', 'methods', 'image']  # Include the image field


        widgets = {
            'methods': forms.Textarea(attrs={'rows': 4}),
        }


from django import forms
from .models import CaretakerSlot

class CaretakerSlotForm(forms.ModelForm):
    class Meta:
        model = CaretakerSlot
        fields = ['service', 'duration', 'base_price', 'price_per_day', 'image']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CaretakerSlotBooking

class CaretakerSlotBookingForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('Pet Sitting', 'Pet Sitting'),
        ('Pet Grooming', 'Pet Grooming'),
        ('Dog Walker', 'Dog Walker'),
        ('Pet Feeder', 'Pet Feeder'),
    ]

    service = forms.MultipleChoiceField(choices=SERVICE_CHOICES, widget=forms.CheckboxSelectMultiple)
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Duration in days'}))
    pet_name = forms.CharField(max_length=100)
    pet_breed = forms.CharField(max_length=100)
    pet_species = forms.CharField(max_length=100)
    pet_age = forms.IntegerField()
    pet_image = forms.ImageField(required=False)
    service_start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    additional_notes = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Any special requests'}), required=False)

    class Meta:
        model = CaretakerSlotBooking
        fields = ['service', 'duration', 'additional_notes', 'pet_name', 'pet_breed', 'pet_species', 'pet_age', 'pet_image', 'service_start_date']

    def clean_pet_age(self):
        pet_age = self.cleaned_data.get('pet_age')
        if pet_age < 0:
            raise ValidationError("Pet age cannot be negative.")
        return pet_age

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration < 1:
            raise ValidationError("Duration must be at least 1 day.")
        return duration

    def clean_service_start_date(self):
        service_start_date = self.cleaned_data.get('service_start_date')
        if service_start_date < timezone.now().date():
            raise ValidationError("Service start date cannot be in the past.")
        return service_start_date

    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('service', [])
        duration = cleaned_data.get('duration', 0)

        if services and duration:
            total_price = self.calculate_price()
            if total_price < 0:
                raise ValidationError("Total price cannot be negative.")

        return cleaned_data

    def calculate_price(self):
        prices_per_day = {
            'Pet Sitting': 100,
            'Pet Grooming': 150,
            'Dog Walker': 75,
            'Pet Feeder': 50,
        }

        services = self.cleaned_data.get('service', [])
        duration = self.cleaned_data.get('duration', 0)

        total_price = sum(prices_per_day[service] * duration for service in services)
        return total_price
