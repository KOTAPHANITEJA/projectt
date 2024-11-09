from django.contrib.auth.forms import UserCreationForm 
from django import forms  
from django.contrib.auth.models import User
from django.forms.widgets import DateInput
#from .models import Booking

class CreateUserForm(UserCreationForm): 
    class Meta: 
        model=User 
        fields=["username","email","password1","password2"]

