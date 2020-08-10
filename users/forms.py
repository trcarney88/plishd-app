from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        labels = {'jobTitle':'Job Title', 'company':'Company', 'reminderTime':'Time', 'timezone':'Time Zone', 'accompInterval':'Interval', 'notificationType':'Type', 'enabled':'On', 'mobileNumber': 'Mobile Number', 'countryCode': 'Country Code'}
        fields = ['jobTitle', 'company', 'reminderTime', 'timezone', 'accompInterval','notificationType', 'enabled', 'mobileNumber', 'countryCode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
    
