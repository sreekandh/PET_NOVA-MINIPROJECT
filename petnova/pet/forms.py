# forms.py

from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'age', 'breed', 'description', 'category','image']



from django import forms
from .models import UserPet

class UserPetForm(forms.ModelForm):
    class Meta:
        model = UserPet
        fields = ['pet_name', 'pet_breed', 'pet_species', 'pet_age', 'pet_image']

    # Additional validation for fields
    def clean_pet_name(self):
        pet_name = self.cleaned_data.get('pet_name')
        if not pet_name.isalpha():
            raise forms.ValidationError("Pet name should only contain letters.")
        return pet_name

    def clean_pet_breed(self):
        pet_breed = self.cleaned_data.get('pet_breed')
        if not pet_breed.isalpha():
            raise forms.ValidationError("Pet breed should only contain letters.")
        return pet_breed

    def clean_pet_species(self):
        pet_species = self.cleaned_data.get('pet_species')
        if not pet_species.isalpha():
            raise forms.ValidationError("Pet species should only contain letters.")
        return pet_species
