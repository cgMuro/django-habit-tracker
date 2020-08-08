from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Habit

class RegisterForm(UserCreationForm):
    # Add email and placeholders to UserCreationForm 
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.fields.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
        }

# Habit form
class HabitForm(forms.ModelForm):
    activity = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(
            attrs={ 'placeholder': 'Enter activity', 'class': 'form-control form-control-lg' }
        )
    )
    time_spent = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(
            attrs={ 'placeholder': 'Enter time spent', 'class': 'form-control form-control-lg' }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={ 'placeholder': 'Write description here...', 'class': 'form-control form-control-lg' }
        ), 
    )

    class Meta:
        model = Habit
        fields = ('activity', 'time_spent', 'description')