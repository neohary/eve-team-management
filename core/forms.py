from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import generalInfo,donateInfo
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        
        
class newLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField()
    
class donateInfoForm(ModelForm):
    class Meta:
        model = donateInfo
        fields = ('donater','amount','type','info')