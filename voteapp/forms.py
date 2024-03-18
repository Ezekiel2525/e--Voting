from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=6)
    email = forms.EmailField()
    department = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'student_id', 'email', 'department', 'password1', 'password2']