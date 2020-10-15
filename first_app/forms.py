from django import forms 
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo
from django.core import validators 
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    verify_password = forms.CharField(label="Enter your password again", widget=forms.PasswordInput())

    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        vpassword = all_clean_data['verify_password']

        if password != vpassword:
         
            raise forms.ValidationError(('Make sure password match'))
            
            
    class Meta():
        model = User
        fields = ('username','email','password')



class UserToken(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('user_token',)