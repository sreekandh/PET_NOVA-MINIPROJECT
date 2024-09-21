"""from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[@$!%*?&#]', password):
            raise forms.ValidationError("Password must include at least one letter, one number, and one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
"""

"""
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[@$!%*?&#]', password):
            raise forms.ValidationError("Password must include at least one letter, one number, and one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

"""
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re  # Ensure this import is included
from .models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[@$!%*?&#]', password):
            raise forms.ValidationError("Password must include at least one letter, one number, and one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password


# forms.py
from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]  # Add 'phone' if it's a custom field
