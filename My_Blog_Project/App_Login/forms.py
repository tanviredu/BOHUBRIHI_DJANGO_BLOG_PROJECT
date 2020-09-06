from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User 
from .models import UserProfile

class SignupForm(UserCreationForm):
    email     = forms.EmailField(required=True,label="",widget=forms.TextInput(attrs={'placeholder':'Email'}))
    username  = forms.CharField(required=True,label="",widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':"Enter Password"}))
    password2 = forms.CharField(required=True,label="",widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password"})) 

    class Meta:
        model  = User
        fields = ('username','email','password1','password2') 

class UserProfileChange(UserChangeForm):
    class Meta:
        model  = User
        fields = ('username','email','first_name','last_name','password')

class ProfilePic(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields =  ('profile_pic',)

    