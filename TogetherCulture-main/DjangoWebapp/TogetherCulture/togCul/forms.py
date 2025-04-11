from django import forms
from .models import CustomUser
from django.contrib.auth.models import User

# forms.py
from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Re-enter Password')

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password', 'confirm_password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

