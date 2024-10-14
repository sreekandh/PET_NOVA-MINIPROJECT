from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should only contain alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain alphabetic characters.")
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r"^[6-9]\d{9}$", phone):  # Indian phone number pattern
            raise forms.ValidationError("Please enter a valid Indian phone number.")
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
    from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from admin_fn.models import Trainer, Caretaker  # Import the Caretaker model

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")

        # Check if the email exists in the User, Trainer, or Caretaker models
        if not User.objects.filter(email=email).exists() and not Trainer.objects.filter(email=email).exists() and not Caretaker.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        # Perform authentication check in the overall form validation
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Attempt to authenticate with the User model first
            user = authenticate(email=email, password=password)
            if user is None:
                # If no user found in User model, check in Trainer model
                try:
                    trainer = Trainer.objects.get(email=email)
                    # Since the password is not hashed, we directly compare it
                    if trainer.password != password:
                        raise forms.ValidationError("Invalid email or password.")
                except Trainer.DoesNotExist:
                    # If no trainer found, check in Caretaker model
                    try:
                        caretaker = Caretaker.objects.get(email=email)
                        # Since the password is not hashed, we directly compare it
                        if caretaker.password != password:
                            raise forms.ValidationError("Invalid email or password.")
                    except Caretaker.DoesNotExist:
                        raise forms.ValidationError("Invalid email or password.")

        return cleaned_data


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']  # Adjust fields as necessary


