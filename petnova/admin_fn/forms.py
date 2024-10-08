from django import forms
from .models import Cat, Dog

# Form for Cat model
class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'description', 'image']  # Adjust the fields based on your Cat model

# Form for Dog model
class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'age', 'breed', 'description', 'image']  # Adjust the fields based on your Dog model


from django import forms
from .models import AdoptionApplication

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ['full_name', 'phone', 'email', 'address']


from django import forms
from .models import Trainer

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['trainer_name', 'email', 'phone', 'experience', 'specialization', 'image']

from django import forms
from .models import Caretaker

class CaretakerForm(forms.ModelForm):
    class Meta:
        model = Caretaker
        fields = ['caretaker_name', 'email', 'phone', 'experience', 'specialization', 'image']
