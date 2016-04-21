from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        #fields = '__all__'

